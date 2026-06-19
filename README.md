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