# Gitflow do Projeto

Master -> Branch de PRD. Alterada a cada sprint; <br>
Develop -> Branch criada para subir os códigos para o ambiente dev. É atualizado com base na Master a cada sprint; <br>
Release/data-sprint -> Branch criada no inicio da sprint. Códigos que foram testados são colocados nela. Seria nossa branch de HML. <br>

Fluxo:<br>
Criar branch a partir da Master -> Adicionar suas alterações -> Mergear a sua branch na develop (cuidado para não fazer o inverso) -> <br>
Testar na develop em conjunto com outras alterações -> Mergear a branch que foi criada com base na Master para a Release -> <br>
Ao fim apresentar sprint mergear o que foi feito na branch de release para a master e recriar a develop com base na master.
