 kubectl set image deployment.apps/webdb webdb=khaldountaktak/flask-web:5 -n ktaktak
  kubectl set image deployment.apps/webnodb webnodb=khaldountaktak/flask-nodb:2 -n ktaktak

  kubectl rollout status deployment/webdb -n ktaktak
kubectl rollout status deployment/webnodb -n ktaktak
