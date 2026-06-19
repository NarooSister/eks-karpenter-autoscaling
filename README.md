# EKS Karpenter Autoscaling Project

AWS EKS 환경에서 Helm 기반 애플리케이션 배포, HPA 기반 Pod 자동 확장, Karpenter 기반 Node 자동 확장을 실습하는 프로젝트입니다.

이 프로젝트의 목표는 단순히 EKS에 애플리케이션을 배포하는 것이 아니라, 트래픽 증가 상황에서 Pod와 Node가 각각 어떤 기준으로 확장되는지 직접 확인하고 설명할 수 있게 되는 것입니다.

---

## Architecture

```text
Client
  → FastAPI Service
  → Pod
  → HPA scales Pod replicas
  → Pending Pods occur when Node capacity is insufficient
  → Karpenter provisions EC2 Nodes
  → Pending Pods are scheduled on new Nodes
```
---

## Learning Goals
- EKS 클러스터 구성
- Helm 기반 애플리케이션 배포
- Metrics Server 설치
- HPA 기반 Pod 자동 확장
- Karpenter 기반 Node 자동 확장
- 부하 테스트를 통한 확장 확인
- eksctl 기반 구성을 Terraform으로 전환

---

## Phases
### Phase 1. eksctl

eksctl을 사용해 EKS 클러스터를 빠르게 구성하고, HPA와 Karpenter의 동작 흐름을 확인합니다.

### Phase 2. Terraform

Phase 1에서 검증한 구조를 Terraform으로 재구성해 재현 가능한 인프라 코드로 전환합니다.

---

## Tech Stack
- AWS EKS
- eksctl
- Terraform
- Kubernetes
- Helm
- HPA
- Karpenter
- FastAPI
- Docker
- k6

---

## Current Result

현재 Phase 1에서는 EKS 클러스터를 생성하고, FastAPI 애플리케이션을 ECR 이미지 기반으로 Helm 배포했습니다.

배포된 애플리케이션은 `ClusterIP` Service와 `kubectl port-forward`를 통해 응답을 확인했습니다.

```text
Local Request
  → kubectl port-forward
  → Kubernetes Service
  → FastAPI Pod
```

---

## HPA Scale-out Test

HPA는 CPU 사용률 60%를 기준으로 Pod 수를 조정하도록 설정했습니다.

```yaml
minReplicas: 2
maxReplicas: 10
targetCPUUtilizationPercentage: 60
```

`/cpu` 엔드포인트에 부하를 발생시킨 결과, CPU 사용률이 target을 초과하면서 Replica 수가 2개에서 9개까지 증가했습니다.

![HPA Scale Test](image/hpa_test_01.png)

```text
cpu: 2%/60%     replicas: 2
cpu: 241%/60%   replicas: 3
cpu: 245%/60%   replicas: 6
cpu: 251%/60%   replicas: 9
```

부하가 종료된 후에도 Replica 수는 즉시 감소하지 않았습니다.
이를 통해 HPA는 scale-out에는 빠르게 반응하지만, scale-in은 안정성을 위해 일정 시간 지연된다는 것을 확인했습니다.

---

## Pending Pod Analysis

HPA가 Pod를 9개까지 늘렸지만, 일부 Pod는 Pending 상태가 되었습니다.

```text
0/1 nodes are available: 1 Too many pods.
```

원인은 CPU/Memory 부족이 아니라, `t3.small` 노드의 Pod 개수 제한이었습니다.

```text
Node pod capacity: 11
Running pods: 11
```

이 실습을 통해 HPA와 Karpenter의 역할 차이를 확인했습니다.

```text
HPA
  → Pod replica 수 증가

Karpenter
  → Pending Pod를 감지하고 Node 생성
```

---

## Key Takeaways

* HPA는 Metrics Server의 CPU 메트릭을 기반으로 Pod replica 수를 조정한다.
* HPA는 Node를 직접 늘리지 못하므로, Node 용량이 부족하면 Pod는 Pending 상태가 된다.
* 작은 인스턴스에서는 CPU/Memory보다 Pod 개수 제한이 먼저 병목이 될 수 있다.
* 운영 환경에서는 scale-out 속도뿐 아니라 scale-in 안정화 시간도 고려해야 한다.
* 다음 단계에서는 Karpenter를 설치해 Pending Pod 발생 시 EC2 Node가 자동 생성되는지 검증한다.
