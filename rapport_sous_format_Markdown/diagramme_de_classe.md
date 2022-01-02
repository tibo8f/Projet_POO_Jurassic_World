

|Item |
| - |
|+line +column +round\_alive |
||

|World |
| - |
|+nbline +nbcolumn +nbcase +empty\_case +board +round\_number +parametre |
|+affichage\_plateau() +get\_board() +round() +change\_item() +remove\_item() +add\_item() +move\_item() |
0..\*  1 



|LifeForm |
| - |
|+health +energy +already\_played +vision |
|+energy\_loss() +health\_loss() |

|Meat |
| - |
|+symbol +waitaround +image |
|+die() |

|OrganicWaste |
| - |
|+symbol +waitaround +image |
||
1 

1 

|Zone |
| - |
|+board +line +column |
|+vision\_en\_cercle() +contact\_zone() +move\_zone() |

|Animals |
| - |
|<p>+genre </p><p>+gestation +round\_in\_gestation </p>|
|+die() +reproduction() +poop() |

|Plant |
| - |
|+waitaround +semis\_zone +raciness\_zone |
|<p>+die() </p><p>+feed() +reproduction() </p>|


|Tree |
| - |
|+symbol +health +energy +image |
||

|Bush |
| - |
|+symbol +health +energy +image |
||
 

|Rose |
| - |
|+symbol +health +energy +image |
||

|Carnivore |
| - |
|+attack\_damage |
|+attack() +feed() +move() |

|Herbivore |
| - |
||
|+feed() +move() |


|Tyrannosaure |
| - |
|<p>+symbol +health </p><p>+energy </p><p>+vision +attack\_damage +image </p>|
||
 

|Velociraptor |
| - |
|<p>+symbol +health </p><p>+energy +attack\_damage +image </p>|
||
 

|Brachiosaure |
| - |
|+symbol +health +energy +image |
||
 

|Stegosaure |
| - |
|+symbol +health +energy +vision +image |
||

