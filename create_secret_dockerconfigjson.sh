#!/bin/bash
# Usage: ./create_secret_dockerconfigjson.sh REGISTRY USER TOKEN NAMESPACE

GITlAB_REGISTRY="$1"
GITLAB_USER="$2"
GITLAB_TOKEN="$3"
NAMESPACE="$4"

echo GITlAB_REGISTRY=$GITlAB_REGISTRY
echo GITLAB_USER=$GITLAB_USER
echo GITLAB_TOKEN=$GITLAB_TOKEN
echo NAMESPACE=$NAMESPACE

cat > .dockerconfigjson << EOF
{
  "auths": {
    "$GITlAB_REGISTRY": {
      "auth": "$(echo -n "$GITLAB_USER:$GITLAB_TOKEN" | base64)"
    }
  }
}
EOF

kubectl create secret generic gitlab-deploy-token \
    --namespace $NAMESPACE \
    --from-file=.dockerconfigjson \
    --type=kubernetes.io/dockerconfigjson