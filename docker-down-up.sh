#!/bin/bash
echo "コマンド [ docker-compose down ] を実行中..."
docker-compose down
echo "コマンド [ docker-compose down ] 完了"

echo "コマンド [ docker-compose up -d ] を実行中..."
docker-compose up -d
echo "コマンド [ docker-compose up -d ] 完了"