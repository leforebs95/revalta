#!/bin/bash

# Parse command line arguments
REGION="us-west-2" # Default value
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
    --git-branch)
        GIT_BRANCH="$2"
        shift
        ;;
    --region)
        REGION="$2"
        shift
        ;;
    *)
        # Unknown option
        echo "Unknown option: $key"
        exit 1
        ;;
    esac
    shift
done

# Put in your own ECR repository URI
ECR_DOMAIN="975049886332.dkr.ecr.$REGION.amazonaws.com"
NGINX_URI="nivalta_nginx"
SVELTE_URI="nivalta_ui_server"
FLASK_URI="nivalta_web_server"

# Define an array of URIs
URIS=(
    $NGINX_URI
    $SVELTE_URI
    $FLASK_URI
)

# aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_DOMAIN

# Iterate over the URIs and perform the desired operations
# for URI in "${URIS[@]}"; do
#     # Docker Login

#     # Build and push the container image using Docker CLI
#     docker build -t $URI .
#     docker tag $URI:$GIT_BRANCH $ECR_DOMAIN/$URI:$GIT_BRANCH
#     docker push $ECR_DOMAIN/$URI:$GIT_BRANCH

# done

# Build a container definitions
CPU=256
MEMORY=512

NGINX_IMAGE_URL="$ECR_DOMAIN/$NGINX_URI:$GIT_BRANCH"
NGINX_TEMPLATE_FILE="../infra/nginx_container.template.json"
NGINX_CONTAINER=$(
    jq \
        --arg image "$NGINX_IMAGE_URL" \
        --arg cpu "$CPU" \
        --arg memory "$MEMORY" \
        '.image = $image | .cpu = $cpu | .memory = $memory' \
        $NGINX_TEMPLATE_FILE
)

SVELTE_IMAGE_URL="$ECR_DOMAIN/$SVELTE_URI:$GIT_BRANCH"
SVELTE_TEMPLATE_FILE="../infra/svelte_container.template.json"
SVELTE_CONTAINER=$(
    jq \
        --arg image "$SVELTE_IMAGE_URL" \
        --arg cpu "$CPU" \
        --arg memory "$MEMORY" \
        '.image = $image | .cpu = $cpu | .memory = $memory' \
        $SVELTE_TEMPLATE_FILE
)

FLASK_IMAGE_URL="$ECR_DOMAIN/$FLASK_URI:$GIT_BRANCH"
FLASK_TEMPLATE_FILE="../infra/flask_container.template.json"
FLASK_CONTAINER=$(
    jq \
        --arg image "$FLASK_IMAGE_URL" \
        --arg cpu "$CPU" \
        --arg memory "$MEMORY" \
        '.image = $image | .cpu = $cpu | .memory = $memory' \
        $FLASK_TEMPLATE_FILE
)

# Ensure CONTAINER_DEFINITIONS is a proper JSON string
CONTAINER_DEFINITIONS=$(
    jq -n \
        --argjson svelte "$SVELTE_CONTAINER" \
        --argjson flask "$FLASK_CONTAINER" \
        --argjson nginx "$NGINX_CONTAINER" \
        '[$svelte, $flask, $nginx]'
)

TASK_DEFINITION_FILE="../infra/web_nginx_definition.template.json"

TASK_DEFINITION=$(
    jq \
        --argjson containers "$CONTAINER_DEFINITIONS" \
        '.containerDefinitions = $containers' \
        $TASK_DEFINITION_FILE
)

echo $TASK_DEFINITION

# # Register a new task definition revision
# TASK_DEFINITION_ARN=$(
#     aws ecs register-task-definition \
#         --cli-input-json "$TASK_DEFINITION" \
#         --query 'taskDefinition.taskDefinitionArn' \
#         --output text
# )

# # Update an ECS service to use this task definition.
# CLUSTER="default"
# SERVICE="my-app"

# aws ecs update-service \
#     --cluster $CLUSTER \
#     --service $SERVICE \
#     --task-definition $TASK_DEFINITION_ARN
