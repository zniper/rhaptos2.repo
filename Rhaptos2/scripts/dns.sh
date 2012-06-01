for h in devweb devjenkins devlog www cdn repo
do

  echo $h
  echo \ \ \   `dig +short $h.office.mikadosoftware.com`

done

