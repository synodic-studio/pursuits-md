# Example Pursuits

Set up a desk for writing and video calls.

<!-- pursuits-md:graph -->
```mermaid
flowchart LR
    subgraph horizontal[" "]
        direction LR
        TDSK["Desk Setup<br/><code>DSK</code> 🟢 Working"]
        TNV7["Equipment Inventory<br/><code>NV7</code> 🔵 Done"]
        TMAT[["Desk Mat<br/><code>MAT</code> ⚪ Open"]]
        TDSK --> TNV7
        TDSK --> TMAT
    end
    style horizontal fill:none,stroke:none,stroke-width:0px;
    click TDSK "https://github.com/synodic-studio/pursuits-md/blob/v0.1.1-clarifications/examples/demo-vault/pursuits/DSK%20-%20Desk%20Setup.md"
    click TNV7 "https://github.com/synodic-studio/pursuits-md/blob/v0.1.1-clarifications/examples/demo-vault/pursuits/DSK/NV7%20-%20Equipment%20Inventory.md"
    click TMAT "https://github.com/synodic-studio/pursuits-md/blob/v0.1.1-clarifications/examples/demo-vault/pursuits/DSK/MAT%20-%20Desk%20Mat.md"
    classDef openTicket stroke:#818994,stroke-width:2px;
    class TMAT openTicket;
    classDef workingTicket stroke:#389364,stroke-width:2px;
    class TDSK workingTicket;
    classDef doneTicket stroke:#4185ba,stroke-width:2px;
    class TNV7 doneTicket;
```

<!-- pursuits-md:graph-links -->

1. [Desk Setup](https://github.com/synodic-studio/pursuits-md/blob/v0.1.1-clarifications/examples/demo-vault/pursuits/DSK%20-%20Desk%20Setup.md)
2. [Equipment Inventory](https://github.com/synodic-studio/pursuits-md/blob/v0.1.1-clarifications/examples/demo-vault/pursuits/DSK/NV7%20-%20Equipment%20Inventory.md)
3. [Desk Mat](https://github.com/synodic-studio/pursuits-md/blob/v0.1.1-clarifications/examples/demo-vault/pursuits/DSK/MAT%20-%20Desk%20Mat.md)

<!-- /pursuits-md:graph-links -->
