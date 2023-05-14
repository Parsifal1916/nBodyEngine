# nBodyEngine
## Descrizione
nBodyEngine è un modulo open-source per simulare il celebre n-Body Problem, le orbite di pianeti attorno alla propria stella e, in versioni future, materia in caduta verso un buco nero supermassivo. Le seguenti librerie sono richieste per eseguire il modulo correttamente:
- **matplotlib**
- **numpy**
## Code Overwiev
### Classe Body
La classe **nBodyEngine.Body** è usata per rappresentare corpi celesti. Questa classe richiede due liste, la prima è composta dai seguenti argometi (in ordine):
- Massa del corpo
- posizione x (in metri)
- posizione y (in metri)
- velocità x (m/s)
- velocità y (m/s)
- (facoltativo) colore del marker rappesentato nel grafico

La seconda lista contiene tutti gli **nBodyEngine.Body** presenti nella simulazione

La classe contiene le seguenti funzioni:

- **nBodyEngine.Body.update(dt)**: Aggiorna posizione (**self.x** e **self.y**) a seconda del valora della velocità (**self.vx** e **self.vy**)

- **nBodyEngine.Body.net_force()**: Calcola la forza agente di tutti gli altri corpi nella simulazione sul corpo in questione. Ritorna due   **float** (**nBodyEngine.Body.fy** e **nBodyEngine.Body.fx**)

- **nBodyEngine.Body.GetDistance(x, y)**: Calcola la distanza tra il corpo in questione e una la coordinata inserita. Viene utilizzato per calcolare l'attrazione gravitazionale tra i corpi

- **nBodyEngine.Body.getDirectionVector(x, y)**: calcola le componenti x e y di una forza proveniente dalla coordinate inserite 

### GraphEngine.py
Questo script contiene la classe **Graph** che richiede come argomenti (in ordine):
- **bodies**, una lista di tutti i corpi contenuti nella simulazione
- **graphLimits**, un float che rappresenta le dimensioni del grafico

La classe contiene le suguenti funzioni

- **nBodyEngine.Graph.updateScreen()**: Pulisce lo schermo e reimposta le dimensioni del grafico

- **nBodyEngine.Graph.animate()**: viene chiamata automaticamente da matplotlib, aggiorna la posizione di tutti i corpi con il loro metodo **update()**

- **nBodyEngine.Graph.start(timescale)**: Da il via alla simulazione, richiede un parametro (timescale) che rappresenta la velocità della simulazione
