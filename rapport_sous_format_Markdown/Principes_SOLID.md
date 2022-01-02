Principes SOLID 

**1er principe :** Single Responsibility Principle (SRP) 

Nous avons respecté ce principe en séparant chaque fonctionnalité de l’écosystème en classes. Ainsi chaque classe a une responsabilité unique. 

Par exemple, la classe « zone » est la seule classe à s’occuper de déterminer la zone et n’a aucune autre responsabilité. 

**2ème principe :** Liskov Substitution Principle (LSP)

Nous avons respecté ce principe en faisant en sorte que chaque classe fille conserve les fonctionnalités de sa classe mère et ne remplace aucune fonctionnalité fournie par sa classe mère. 

Par exemple, nous n’avons pas créé une fonction « feed() » pour toutes les formes de vies directement dans la classe « LiveForm » malgré qu’elles doivent toutes se nourrir pour éviter de devoir transformer cette fonction dans ses classes filles (ayant des régimes différents). Nous avons donc créé une fonction feed() différente dans chaque classe fille (classe Plant, Herbivore et Carnivore). 
