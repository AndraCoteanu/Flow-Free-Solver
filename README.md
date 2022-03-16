# Documentatie[^1] - Flow Free Game Solver 
## Artificial Intelligence, 3rd year, FII
### @authors: Coteanu Andra, Marele Carina, Mihaes Antonio, Rotariu Cosmin (grupa 3A4)

----------------------------------------------------------------
### Cerinta

Un agent care rezolva puzzle-ul Flow.
- Flow are loc pe o grila 2D cu n linii și m coloane.
- Fiecare puzzle are un număr de C culori.
- In starea initiala sunt 2 * C pozitii colorate, cate doua pentru fiecare culoare.
- Scopul este sa conectati pozițiile de aceeași culoare.
- Drumurile care fac legăturile sunt formate din segmente paralele cu axele.
- Drumurile nu se pot intersecta.
- Este preferabil sa puteți procesa o imagine a unei stări inițiale din Flow pentru a construi datele de intrare.
- Legături relevante:
https://www.microsoft.com/de-de/p/flow-free/9wzdncrdqvpj

----------------------------------------------------------------

## Generare de puzzle-uri[^2]
### @author: Antonio M.

Pentru a se genera puzzle-urile s-a creat un script folosind limbajul python "screen_scan.py" care:
- va crea folderul "puzzles" daca acesta nu exista deja, daca exista va ignora acest pas si va continua sa adauge fisiere de tip json in el
- utilizatorul va trebui apoi sa introducă numele pachetului din care fac parte puzzle-urile pe care vrea sa le salveze
- utilizatorul acestui scrip va fi întrebat ce dimensiune au acest tip de puzzle pe care vrea sa le converteasca in json
- utilizatorul va trebui apoi sa poziționeze cursorul peste butonul "next" (pentru a putea fi salvate coordonatele acestuia)
- utilizatorul va introduce cate puzzle-uri vrea sa obtina
- pentru fiecare puzzle se va crea un nou fisier json in care se vor pune culorile pentru fiecare "casuta" din puzzle
- daca inca nu s-a atins numarul cerut de puzzle-uri atunci se va da click automat pe butonul de next folosind coordonatele[^3]

----------------------------------------------------------------
## Caracteristicile jocului Flow Free[^4]

Flow Free este un joc bazat in jurul rezolvarii unui puzzle: arata ca o matrice cu dimensiuni de n x n pe care se afla mai multe perechi de cate 2 puncte colorate. Scopul jocului si al acestui proiect este rezolvarea unor astfel de puzzle-uri astfel incat:
- toate punctele de aceeasi culoare sa fie unite de un singur drum neintrerupt de alte drumuri
- toate drumurile sa ocupe toate spatiile de pe tabla afisata

![image](https://user-images.githubusercontent.com/72747266/147162193-f0e8206a-c073-407f-b3ff-206b84f2bca2.png)

Un prim pas de rezolvare, indiferent de algoritmul folosit, este sa decidem cu care culoare incepem algoritmul. Cel mai eficient este sa incepem cu acele culori care au cele mai putine optiuni de deplasare.

Dupa mai mult research si analiza in mediul online a acestui tip de puzzle am ajuns la concluzia ca 2 posibili algoritmi de rezolvare care ar fi foarte eficienti sunt reducerea problemei la SAT si folosirea unei euristici cu A*. 

Euristici aplicabile pot fi folosind algoritmul lui Djikstra, BFS, DFS, etc. 

Un alt algoritm care ar putea rezolva acest tip de problema este backtracking, dar pentru ca el genereaza si incearca toate posibilitatile pana o gaseste pe cea corecta putem deduce ca nu este eficient ca timp.

----------------------------------------------------------------

## Utilizare

Se pot rula fișierele `sat_solver.py` și `heuristic_solver.py`. Acestea primesc de la utilizator numele unui fișier JSON. Acest fișier va fi o listă de liste unde un element liber este reprezentat prin `null`, iar dacă două elemente au aceeași valoare, atunci ele reprezintă aceeași culoare. Exemplu:

```json
[
  [null,  null,    null, null,     null],
  [null,  "blue",  null, "blue",   "green"],
  [null,  null,    null, null,     null],
  ["red", "green", null, "purple", "red"],
  [null,  null,    null, null,     "purple"]
]
```

----------------------------------------------------------------

## Reducere la SAT[^5]
### @author: Antonio M. , Andra C.

Problema SAT[^6] este problema de a determina daca exista macar o formula din logica booleana care poate fi interpretata astfel incat cel putin odata aceasta sa rezulte TRUE.

Reamintim Forma Normala Conjunctiva (FNC): mai multe disjunctii unite prin conjunctie. Exemplu: ![image](https://user-images.githubusercontent.com/72747266/147168402-95e6e443-2576-428c-92a8-3cf2416b064a.png)

### Reducerea FlowFree la SAT

Pentru a face aceasta reducere vom avea nevoie de FNC pentru ca vom lua fiecare constrangere/cerinta si o vom scrie sub forma de logica booleana respectand FNC.

Pentru a putea demonstra ca acest tip de puzzle poate fi rezolvat cu SAT, mai intai vom face cateva notatii:

- puzzle-ul este de dimensiunea `n x n` => vom avea ![equation](http://www.sciweavers.org/tex2img.php?eq=%20n%5E%7B2%7D%20&bc=Black&fc=White&im=jpg&fs=12&ff=arev&edit=0) patratele
- numarul de culori il vom nota cu `c`
- directiile posibile sunt:
  - sus-jos &emsp; &emsp; &emsp; &emsp; │
  - jos-sus &emsp; &emsp; &emsp; &emsp; │
  - stanga-dreapta  &emsp; ─
  - dreapta-stanga  &emsp; ─
  - sus-stanga &emsp; &emsp; &nbsp;&nbsp; ┘
  - sus-dreapta &emsp; &emsp; └
  - jos-stanga &emsp; &emsp; &nbsp;&nbsp;&nbsp; ┐
  - jos-dreapta &emsp; &emsp;&nbsp; ┌
- observam castanga-dreapta si dreapta-stanga, dar si sus-jos si jos-sus sunt reprezentate identic, deci putem spune ca avem 6 directii, in loc de 8

#### 1. Fiecare patratel are o culoare a sa
- avem `n*n*c` posibilitati de colorare
- fie `i` id-ul patratelelor `(1 <= i <= n*n)`
- avem `c*(c-1)/2` combinatii posibile de culori pentru fiecare patratel care nu este deja colorat de o bulina de start/stop
- pentru cateva patratele avem deja stabilita culoarea deoarece acelea vor fi bulinele de start/stop; pentru un astfel de patrat `i` putem scrie urmatoarea clauza: ![image](https://user-images.githubusercontent.com/72747266/147306787-a288e5b7-7c15-4c9a-9ebe-7476a64346d1.png)
- pentru restul patratelelor pentru care nu au deja culoarea prestabilita putem scrie urmatoarea clauza (pentru un patratel `i`): ![image](https://user-images.githubusercontent.com/72747266/147306585-1ad476b1-8478-4939-a2b0-e9a6016e6630.png)
- fiecare din clauzele de mai sus vin de la: ![image](https://user-images.githubusercontent.com/72747266/147306465-cc62799a-2a17-42d1-8165-e01c777828b6.png) , unde `u` si `u'` sunt doua culori diferite pentru patratelul `i` (in formulele prezentate mai sus aceasta clauza este negata deoarece am adus clauza la forma normala conjunctiva)

#### 2. Fiecare bulina de start/inceput are exact un vecin (drum) cu aceeasi culoare
- fiecare patratel cu bulina de start/stop va avea exact un singur vecin cu drum (cu aceeasi culoare)
- presupunem un patratel cu bulina de start/stop `i` care are culoarea `m` si cei 4 vecini corespunzatori cu punctele cardinale (N,S,E,V) `s, t, u, v`
- pentru ca patratelul `i` are culoarea `m`, atunci putem scrie clauza: ![image](https://user-images.githubusercontent.com/72747266/147349647-0579c2ca-2cc7-47ee-a6c6-44f6a0983b57.png)
- in plus, oricare 2 vecini ai patratelului `i` nu pot avea aceeasi culoare
  - pentru a compara daca 2 patrate au aceeasi culoare putem scrie clauza: ![image](https://user-images.githubusercontent.com/72747266/147349787-9f490b95-1c8c-4d58-aa2c-ec049c1e635b.png)
  - insa pe noi ne intereseaza ca atunci cand 2 patrate au aceeasi culoare sa obtinem rezultatul clauzei FALSE (asa cum e scrisa mai sus clauza, daca 2 patrate au aceeasi culaore returneaza TRUE); pentru a obtine asta va trebui sa negam clauza anterioara, deci vom obtine clauza: ![image](https://user-images.githubusercontent.com/72747266/147350002-dd871b5a-6e3f-40db-8cb0-6f0527339fd4.png)
  - clauza de mai sus este scrisa pentru exemplul dintre patratele `s` si `t` cu culoarea `m`, insa aceeasi clauza se aplica pentru toate combinatiile de cate 2 patrate din `s, t, u, v` cu culoarea `m`: `s si t`, `s si u`, `s si v`, `t si u`, `t si v`, `u si v`
  - nu are rost sa comapram `s si t` si `t si s` deoarece operatiile ^ si v sunt comutative, deci vom obtine practic aceeasi clauza

#### 3. Culoarea bulinelor de start/stop sunt stiute
- putem asigna instant acelor patratele culoarea lor
- deasemenea putem sa eliminam restul culorilor ca o posibilitate pentru patratelul respectiv
- inainte de rezolvarea jocului trebuie sa avem un numar par de patratele ale caror culori le cunoastem, iar numarul lor sa fie dublul numarului de culori

#### 4. Directia drumurilor in casutele care nu sunt buline de start/stop sunt in numar de 8: sus, jos, stanga, dreapta, sus-stanga, sus-dreapta, jos-stanga, jos-dreapta
- fiecare patratel care nu contine o bulina de start/stop va contine, in rezolvarea finala, va avea o singura directie care va indica cu care dintre vecinii sai formeaza un drum
  - faptul ca acest tip de patratel va contine macar o directie poate fi scris ca o clauza pentru fiecare astfel de patratel
  - faptul ca acest tip de patratel nu poate contine mai mult de o singura directie poate fi scris ca `2*nr_directii = 2*6 = 12 clauze` pentru fiecare patratel (daca cele 16 clauze sunt indeplinite atunci este indeplinita si clauza de la subpunctul anterior)
- doua astfel de patratele vecine unite prin directiile pe care le contin vor avea aceeasi culoare
- un astfel de patratel poate avea doar 2 vecini de aceeasi culoare (fie 2 patrate cu directie, fie unul cu directie si unul cu bulina start/stop, fie ambii cu bulina start/stop) 
- toate directiile de aceeas culoare formeaza un drum; drumul trebuie sa inceapa si sa se termine in patratelele cu bulina de aceeasi culoare
- reamintim directiile posibile si cum vor fi aceastea notate:
    - sus-jos &emsp; &emsp; &emsp; &emsp; │
    - jos-sus &emsp; &emsp; &emsp; &emsp; │
    - stanga-dreapta  &emsp; ─
    - dreapta-stanga  &emsp; ─
    - sus-stanga &emsp; &emsp; &nbsp;&nbsp; ┘
    - sus-dreapta &emsp; &emsp; └
    - jos-stanga &emsp; &emsp; &nbsp;&nbsp;&nbsp; ┐
    - jos-dreapta &emsp; &emsp;&nbsp; ┌

#### 5. Vecinul patratelului curent aflat in directia pe care acesta o indica tebuie sa fie de aceeasi culoare
- fiecare patratel trebuie considerat ca o punte intre altele 2, de aceeasi directia pe care o vor contine patratele va simboliza de fapt care 2 patratele vecine le uneste
- pentru orice patratel `i` pe care avem directia `d` vom avea 2 vecini `s si t` care trebuie sa aiba aceeasi culoare ca si patratul `i`
- presupunand ca patratelul `i` are culoarea `m` atunci vom obtine clauza: ![image](https://user-images.githubusercontent.com/72747266/147350782-79ce7488-e3db-4533-bfc3-1f9c7319628a.png)
- pentru ca nu putem traduce acea clauza intr-o secventa de cod asa cum am scris-o mai sus va trebui sa aducem aceasta clauza in forma ei normala conjunctiva
  - clauza de mai sus scrisa in FNC va produce 4 clauze:  
    ![image](https://user-images.githubusercontent.com/72747266/147351220-fcc03cc4-5331-4712-becd-9ef4a90cf3a8.png)

#### 6. Vecinii patratelului curent aflat in oricare alta directie decat cea pe care acesta o indica tebuie sa fie de alta culoare
- toti vecinii ramasi neconectati de drumul din patratel trebuie sa aiba orice alta culoare in afara de culoarea patratelului
- aceasta regula previne ca un drum sa se intercaleze cu el insusi la un moment dat
- pentru un patrat `i` cu directia `d` si culoarea `m`, orice vecin `s` care nu e indicat de directia `d` nu poate avea culoarea `m`: ![image](https://user-images.githubusercontent.com/72747266/147359857-810bd592-ad5f-4dea-8f08-6ec563d0b035.png)
  - formula de mai sus trebuie adusa si ea in FNC si obtinem clauza: ![image](https://user-images.githubusercontent.com/72747266/147359910-df08ba9a-1c7c-49d2-8020-9c929497a76c.png)

Aplicand aceste reguli pe un puzzle cu `n*n` patratele si `c` culori obtinem `n*n*c` variabile pentru culori si aproape `6*n*n` variabile pentru directii (include si patratelele cu buline de start/stop). Vom avea `O(n*n*c*c)` clauze pentru culori si inca `O(n*n*c)` clauze pentru legaturile dintre culori si directii.

Aceste constrangeri ne ofera cel mai scurt si rapid drum pe care il poate gasi ceea ce poate duce la patratele libere ramase care vor fi umplute cu drumuri. Din experienta obtinuta prin rezolvatul manual al astfel de puzzle-uri am observat ca atunci cand se intampla sa fie extra patratele acestea vor avea un numar par atat pe orizontala cat si pe verticala deoarece trebuie sa ofere posibilitatea de a crea drumuri prin ele. Pentru ca vom avea un numar par de patratee libere vecine si pe orizontala si pe verticala inseamna ca algoritmul acesta ba produce niste cicluri care nu contin buline de start/stop.

![image](https://user-images.githubusercontent.com/72747266/147171137-65b30bb2-2473-4bc2-a3cb-ec9233a07404.png)

Pentru a evita aceste scenarii se mai poate adauga o verificare la solutia finala unde cautam daca exista drumuri astfel incat sa se formeze un ciclu. Exemplu: dreapta-jos, stanga-jos, stanga-sus, dreapta sus: 

┌  ┐  
└  ┘

![image](https://user-images.githubusercontent.com/72747266/147171167-66d05ad3-11b7-4aed-bba7-c2671b0eaf21.png)

Problema SAT are in general, in cel mai rau scenariu, un numar exponential de varabile, deci o complexitate exponentiala. Problema SAT a fost deja demonstrata ca fiind NP-completa, dar in anumite situatii ea poate fi redusa la un timp polinomial, deci incadrata ca o problema P-completa.

### Implementare

#### Limbaj de programare folosit

Pentru realizarea acestui solver am folosit Python 3.10 alaturi de alte cateva module.

Mai multe specificatii pentru aceste module se poate gasi in fisierul .txt[^7].

#### Librarii / Module folosite

- dataclasses[^8]
- enum[^9]
- typing[^10]
- itertools[^11]
- colorama[^12]
- json[^13]
- pysat.formula[^14]
- pysat.solvers[^15]

#### Clase create

- `class Position:`
  - contine 2 variabile de tip int
  - un obiect al acestei clase semnifica coordonatele unui patratel in puzzle: rand si coloana 

- `class FlowDirection(Flag):`
  - definim flaguri pentru directiile pe care le vom folosi
  - metoda `def __str__(self) -> str:` returneaza simbolul aferent fiecarui flag

- `class TileFlowDirection:`
  - aceasta clasa are 2 variabile: una de tip Position si una de tip FlowDirection
  - retine pentru fiecare patratel coordonatele si directia pe care o indica
 
- `class TileColour:`
  - clasa are 2 variabile, una de tip Position si una de tip int
  - retine pentru fiecare patratel coordonatele si culoarea acestuia

- `class Tile:`
  - aceasta clasa are 4 variabile: 
    - una de tip FlowDirection
    - una de tip int
    - una de tip IDPool() (pysat.formula)
    - una de tip int
  - retine pentru fiecare patratel directia pe care o indica si culoarea sa, dar si id-ul obiectului si numarul total de culori

- `class Puzzle:`
  - are 2 variabile, una de tip int si una de tip Tuple[Tuple[Position, Position], ...]
  - metode:
    - `def __post_init__(self):`
      - initializeaza pentru fiecare obiect un ID si memoreaza numarul total de culori accesibile
    - `def positions(self) -> Generator[Position, None, None]:`
      - parcurge intregul puzzle ca pe o matrice
      - "returneaza" generatori ce contin pozitia curenta iterata
    - `def from_file(file_name: str) -> "Puzzle":`
      - se primeste fisierul `.json` 
      - se parcurge fisierul si se va crea o lista de tuple ce va retine pozitia de start si de stop a unei culori
      - se apeleaza constructorul acestei clase si se initializeaza dimensiunea puzzle-ului si tuplele de pozitii de start/stop pentru fiecare culoare
    - `def solve(self) -> Optional[Solution]:`
      - apelam `Minisat22` folosindu-ne de clauzele necesare pentru rezolvarea acestui tip de puzzle
      - daca nu se poate rezolva, functia va returna `None`
      - daca se poate rezolva, atunci se vor pastra intr-o lista variabilele adevarate
      - se parcurge puzzle-ul ca o matrice
      - daca pozitia curenta la care am ajuns prin parcurgere se afla in lista de variabile adevarate, atunci este adaugata la o lista de patratele 
      - parcurgem lista de patratele si adaugam intr-o noua lista (lista de directii) urmatorul element de dupa fiecare element din lista pe care o parcurgem care este de tipul `TileFlowDirection`
      - la fel procedam si pentru culori (lista de culori)
      - adaugam la randul curent patratelul format din lista de directii si cea de culori
      - adaugam la solutie randul curent
      - dupa ce terminam de parcurs puzzle-ul si obtinem cat de cat o solutie verificam daca s-a format vreun ciclu
      - daca s-a format vreun ciclu atunci la mai adaugam o clauza si reluam rezolvarea 
      - daca nu s-a format niciun ciclu atunci putem returna solutia
    - `def print(self) -> None:`
      - se parcurge puzzle-ul si in functie de listele de buline de start/stop si de culori se printeaza ce am obtinut (rezolvarea, daca aceasta exista) 

#### Functii / Metode create

- `def colour_to_escape_sequence(colour: int) -> str:`
  - primeste un numar ca parametru, il transforma in si returneaza codul unei culori
 
- `def print_solution(solution: Solution) -> None:`
  - preia solutia ca parametru si o afiseaza utilizatorului folosind culori si simboluri pentru directia drumurilor
 
- clauze:
  - `def must_have_a_direction(puzzle: Puzzle) -> List[Clause]:`
    - se parcurg toate pozitiile si pentru fiecare se verifica daca au o directie
    - daca au directie se va adauga id-ul lor in lista de clauze
 
  - `def must_have_a_colour(puzzle: Puzzle) -> List[Clause]:`
    - se parcurg toate pozitiile si pentru fiecare se verifica daca au o culoare
    - daca au o culoare se va adauga id-ul lor in lista de clauze
 
  - `def must_not_have_two_directions(puzzle: Puzzle) -> List[Clause]:`
    - se parcurg toate pozitiile si se mai parcurg si combinari luate cate 2 de directii
    - se adauga in lista de clauze id-ul directiei de la pozitie cu prima pozitie si apoi id-ul directiei de la pozitie cu a doua directie din combinare
 
  - `def must_not_have_two_colours(puzzle: Puzzle) -> List[Clause]:`
    - se parcurg toate pozitiile si se mai parcurg si combinari luate cate 2 de culori
    - se adauga in lista de clauze id-ul culorilor patratelelor de la pozitia curenta cu prima culaore si apoi cu a doua culoare
 
  - `def must_not_flow_outside(puzzle: Puzzle) -> List[Clause]:`
    - `def tile_must_not_flow_outside(position: Position, outside: FlowDirection) -> None:` - adauga intr-o lista locala de clauze toate id-urile pentru care directia indica exteriorul puzzle-ului
    - se parcurge puzzle-ul si pentru fiecare element se verifica daca iese din puzzle fie prin nord, sud, est sau vest cu functia definita anterior (care va adauga clauzele necesare in lista)
    - se vor returna clauzele
 
  - `def only_endpoints_flow_one_way(puzzle: Puzzle) -> List[Clause]:`
    - se parcurg positiile din puzzle
    - daca pozitia este una a unei buline de start/stop se verifica daca directia ei este sus, jos, stanga sau dreapta
    - daca da se adauga id-ul in lista de clauze
    - daca pozitia nu este de start/stop atunci se verifica daca directia este sus-jos, stanga-dreapta, sus-stanga, sus-dreapta, jos-stanga sau jos-dreapta
    - daca da se adauga id-ul in lista de clauze
 
  - `def endpoints_must_have_their_initial_colour(puzzle: Puzzle) -> List[Clause]:`
    - se parcurge lista de perechi de buline de start/stop si pentru fiecare se ia tuplul de pozitii start si stop si culoare si i se adauga id-ul in lista de clauze
 
  - `def tiles_flowing_into_each_other_match(puzzle: Puzzle) -> List[Clause]:`
    - se ia o lista locala de clauze 
    - `def neighbour_matches( position: Position, match_flow: FlowDirection, neighbour_position: Position, neighbour_match_flow: FlowDirection, ) -> None:`
      - parcurge toate directiile si adauga in lista de clauze id-ul directiei de la pozitia `x` cu directia `d` si id-ul directiei de la pozitia `x+1` (`x+1` este vecinul lui `x`) si cu directia `d'` a acestuia 
      - scopul este ca cele 2 directii vecine trebuie sa se potriveasca cumva
      - se parcurg apoi culorile existente in general in puzzle
      - se adauga la clauze id-ul obiectului format din pozitie si directie, apoi id-ul obiectului format din pozitie si culoare si apoi id-ul obiectului format din pozitia vecinului si culoare
    - se parcurg pozitiile din puzzle si pentru fiecare pozitie se calculeaza vecinii ei
    - folosindu-ne de functia `neighbour_matches` descrisa mai sus vom adauga clauzele necesare puzzle-ului nostru in lista de clauze
 
  - `def find_cycles(puzzle: Puzzle, solution: Solution) -> List[Clause]:`
    - `def component(position: Position, visited_previously: List[Position] = []) -> List[Position]:`
      - verificam mai intai daca o pozitie a fost deja vizitata
      - daca da returnam acea pozitie, daca nu continuam:
      - salvam separat directia, daca a fost vizitat si care este urmatoarea pozitie
      - pacurgem toate directiile posibile pentru a gasi urmatoarea potentiala directie
      - daca gasim o pozitie care nu a fost vizitata o salvam ca urmatoarea pozitie si iesim din aceasta iteratie
      - daca gasim o urmatoare pozitie returnam daca este vizitat si apelam recursiv aceasta functie
      - daca nu gasim o urmatoare pozitie atunci returnam doar vizitat
    - parcurgem pozitiile de start/stop ale puzzle-ului si apelam functia anterioara pentru fiecare pozitie de start
    - parcurgem apoi toate pozitiile din puzzle si verificam daca au fost sau nu vizitate
    - daca nu a fost vizitata presupunem ca exista un ciclu asa ca apelam din nou functia anterioara de la pozitia nevizitata
    - adaugam si aceste pozitii in lista de pozitii deja vizitate
    - la lista de posibile cicluri adaugam pozitia si directia pentru fiecare patratel
    - functia va returna id-ul pentru fiecare patratel aflat intr-un ciclu pentru a fi adaugat la lista de clauze  

#### Aspecte generale

Flow-ul acestui solver este:

- accesam fisierul puzzle-uri[^16]
- alegem ce puzzle vrem sa rezolvam (categoria si numarul puzzle-ului din acea categorie)
- afisam puzzle-ul ales, care trebuie rezolvat
- rezolvam puzzle-ul folosind metodele si clasele create de noi
- afisam rezolvarea, daca aceasta exista (daca nu exista afisam un mesaj sugestiv)

#### Eficienta

Algoritmul descris de noi, dupa mai multe teste rulate, am observat ca rezolva toate puzzle-urile din cele accesibile noua in aproximativ 0.05 - 0.5 secunde, in functie de dimensiunea si dificultatea puzzle-ului. Numarul de clauze folosite pentru obtinerea rezolvarilor este de ordinul miilor.

![image](https://user-images.githubusercontent.com/72747266/147373695-d8f6d805-7714-4165-a2bb-b0f4a043417f.png)

### Implementare

#### Limbaj de programare folosit

Pentru realizarea acestui solver am folosit Python 3.10 alaturi de alte cateva module.

Mai multe specificatii pentru aceste module se poate gasi in fisierul .txt[^7].

#### Librarii / Module folosite

- typing[^10]
- colorama[^12]
- json[^13]
- termcolor[^17]

#### Functii / Metode create

 - `def print_matrix(matrix): -> Matrix`
   - Printez matricea cu numerele culorilor
 - `def pretty_print_matrix(matrix): -> Colored Matrix`
   - Afisam solutia colorata
 - `def parse_json(file_name1): -> Puzzle Matrix`
   - Parsam puzzle-urile pentru rezolvarea problemei si construiesc matricea cu care vom lucra
 - `def identify_nodes(grid1):`
   - Identifica pozitia nodurilor de start si cele terminale, distantele dintre culorile de acelasi fel
   - Returnam dictionare cu nodurile initiale, cu nodurile finale, cu nodurile corespunzatoare culorile lor si distanta
 - `def checkGrid(matrix):`
   - Functie pentru verificarea validitatii matricii. Daca matricea are un punct(culoare) inconjurata de alte culori,
    adica nu pot pleca din acel punct( forma de T-uri sau + uri)
   - Returnam True daca este in regula, pot pleca din fiecare punct din matrice, False altfel
 - `def solved(matrix):`
   - Verifica daca toate spatiile goale(0) sunt colorate
   - Returnam True daca este colorata, False altfel
 - `def solvePuzzle(matrix):`
   - Functie recursiva pentru verificarea tuturor posibililor mutarii si sarim peste matricile care nu duc la o solutie.
   - Verifica initial daca este valida matricea(daca nu are doar culori in jurul ei, daca pot pleca din acel punct),
     dupa verifica daca este colorata integral matricea, asta insemnand ca am gasit o solutie.
   - Altfel merge la urmatoarea mutare:
   - Verifica daca punctele acestei culori sunt conectate, daca nu sunt, atunci verifica in ce directie trebuie sa
     mearga (stanga, dreapta, sus, jos)
   - Daca din niciuna dintre directii nu rezulta o solutie va returna False, altfel True
    

----------------------------------------------------------------

## BACKTRACKING
### @author: Carina M. , Cosmin R.

Backtracking este un algoritm general de descoperire a tuturor soluțiilor unei probleme de calcul, algoritm ce se bazează pe construirea incrementală de soluții-candidat, abandonând fiecare candidat parțial imediat ce devine clar că acesta nu are șanse să devină o soluție validă.

Pentru a reduce numarul de pasi (bkt) necesari pentru realizarea algoritmului de backtracking, pe urmatoarea matrice se vor aplica urmatoarele reguli:

<img src="https://static.wikia.nocookie.net/wingsoffirefanon/images/2/21/Flow_free_byeogthc.png/revision/latest?cb=20210201210356" width="250">


Incepem rezolvarea puzzle ului prin calcularea distantei TaxiCab intre fiecare pereche de noduri de aceeasi culoare. 

Folosim aceasta informatie pentru a prioritiza nodurile cu o distanta minima. 
De exemplu, pe matricea de mai sus, algoritmul se va focusa pe albastru si mov inchis fiind culorile conectate cu cele mai mici distante.

Cand verificam distanta intre 2 culori, algoritmul verifica 4 directii( dreapta, stanga, sus, jos). Se prioritizeaza directia care reduce cel mai mult distanta TaxiCab intre posibila pozitie a directiei si pozitia finala a culorii(e.g se deplaseaza la stanga prima data daca pozitia finala a culorii se afla in stanga pozitiei curente, pana unde este traseul trasat)

<img src="https://i.imgur.com/Qzi1Ruv.png" width="350">

----------------------------------------------------------------

## Rapoarte finale de analiza. Compararea celor doua implementari
### @author: Andra C. , Carina M., Antonio M., Cosmin R. 

Este clar ca cei doi algoritmi abordeaza altfel acest subiect, deci se vor obtine pasi diferiti, deci timpi diversi de rezolvare. Dar pentru a obtine acesti pasi si codul va varia, deci si acesta poate fi un criteriu de comparatie intre cele doua implementari.

####  Eficienta - timp rezolvare

 - SAT - `O(exp(n)` ~ [0.5, 4] secunde

 - BKT - `O(n!)` ~ [4,20] secunde pentru 9x9 (pentru table mai mici, timpul de rulare scade, iar pentru cele mai mari de 10x10, va dura mai mult rularea algoritmului)

  Este clar ca SAT este **mult mai eficient** decat un BKT.


----------------------------------------------------------------

##### Resurse si alte link-uri utile:

[^1]: [sintaxa fisierelor .md](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) and many more stack**overflow** pages

[^2]: [code](https://github.com/cosminrotariu/Flow_Game/blob/main/screen_scan.py)

[^3]: [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)

[^4]: [FlowFree](https://en.wikipedia.org/wiki/Flow_Free)

[^5]: [code](https://github.com/cosminrotariu/Flow_Game/blob/main/sat_solver.py)

[^6]: [SAT](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)

[^7]: [requirements.txt](https://github.com/cosminrotariu/Flow_Game/blob/main/requirements.txt)

[^8]: [dataclasses](https://docs.python.org/3/library/dataclasses.html)

[^9]: [enum](https://docs.python.org/3/library/enum.html)

[^10]: [typing](https://docs.python.org/3/library/typing.html)

[^11]: [itertools](https://docs.python.org/3/library/itertools.html)

[^12]: [colorama](https://pypi.org/project/colorama/)

[^13]: [json](https://docs.python.org/3/library/json.html)

[^14]: [pysat.formula](https://github.com/pysathq/pysat/blob/master/pysat/formula.py)

[^15]: [pysat.solvers](https://github.com/pysathq/pysat/blob/master/pysat/solvers.py)

[^16]: [folder puzzle](https://github.com/cosminrotariu/Flow_Game/tree/main/puzzles)

[^17]: [termcolor](https://pypi.org/project/termcolor/)
