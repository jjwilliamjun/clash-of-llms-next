# **Guide to Setting Up Node Connections, Node Attributes, and Simulation Settings**

## **Introduction**

This guide is designed to help researchers set up their own node connections, node attributes, and system settings for use in the simulation environment. The setup involves creating three Excel files: one for defining the connections between nodes and their corresponding influence factors, another for specifying node attributes such as alignment, and a third for setting system parameters for the red and blue teams. This guide provides step-by-step instructions on how to format these files, what each column represents, and how to ensure compatibility with the simulation system.

---

## **1. Node Connections File**

### **1.1. Overview**

The Node Connections file defines how each node in the network is connected to other nodes and the strength of those connections (influence factors). The file should be saved as an Excel file with the appropriate sheet name: `NodeConnections`.

### **1.2. File Structure**

| Column           | Description                                              |
| ---------------- | -------------------------------------------------------- |
| Node             | The unique identifier for each node in the network.       |
| Connected_Nodes  | A comma-separated list of nodes directly connected to the node in the first column. |
| Influence_Factor | A comma-separated list of influence factors corresponding to each connected node. |

### **1.3. Example**

| Node   | Connected_Nodes | Influence_Factor |
| ------ | --------------- | ---------------- |
| Node_1 | Node_2, Node_3  | 0.4, 0.3         |
| Node_2 | Node_1, Node_4  | 0.2, 0.5         |
| Node_3 | Node_1          | 0.3              |
| Node_4 | Node_2          | 0.5              |

### **1.4. Instructions**

1. **Open Excel** and create a new workbook.
2. **Rename the first sheet** to `NodeConnections`.
3. **Enter the data** as shown in the example, ensuring that each node's connections and influence factors are correctly listed.
4. **Save the file** with an appropriate name (e.g., `NodeConnections.xlsx`).

### **1.5. Tips**

- Ensure that the `Connected_Nodes` and `Influence_Factor` columns have matching numbers of entries, separated by commas.
- The influence factor should be a value between 0 and 1, where a higher value indicates a stronger influence.

---

## **2. Node Attributes File**

### **2.1. Overview**

The Node Attributes file defines the properties of each node, such as alignment. The file should be saved as an Excel file with the appropriate sheet name: `NodeAttributes`.

### **2.2. File Structure**

| Column    | Description                                                        |
| --------- | ------------------------------------------------------------------ |
| Node_ID   | The unique identifier for each node, consistent with the `Node` column in the Node Connections file. |
| Alignment | A value between representing the initial alignment of the node. |

### **2.3. Alignment Explanation**

The **Alignment** value indicates the initial stance of the node:

- **Alignment ≤ (alignment_min / 2)**: Represents a **Red** alignment, indicating the node is inclined towards the Red side.
- **(alignment_min / 2) < Alignment < (alignment_max / 2)**: Represents a **Neutral** alignment, indicating the node does not strongly favor either side.
- **Alignment ≥ (alignment_max / 2)**: Represents a **Blue** alignment, indicating the node is inclined towards the Blue side.

### **2.4. Example**

| Node_ID | Alignment | 
| ------- | --------- | 
| Node_1  | 0.75      | 
| Node_2  | 0.60      | 
| Node_3  | 0.40      | 
| Node_4  | 0.85      | 

### **2.5. Instructions**

1. **Open Excel** and create a new workbook.
2. **Rename the first sheet** to `NodeAttributes`.
3. **Enter the data** as shown in the example, ensuring that each node's attributes are correctly listed.
4. **Save the file** with an appropriate name (e.g., `NodeAttributes.xlsx`).

### **2.6. Tips**

- Ensure that the `Node_ID` in this file matches the `Node` identifiers in the Node Connections file.
- The `Alignment` values should all be between -1 and 1.

---

## **3. Simulation Settings File**

### **3.1. Overview**

The Simulation Settings file defines parameters for the red and blue teams. It specifies LLMs for both the red and blue teams and the necessary parameters which influence how the models play in the simulation. Models specified in this file must be already connected to the simulation system. The file should be saved as an Excel file with the appropriate sheet name: `SimulationSettings`.
### **3.2. File Structure**

| Column              | Description                                              |
| ------------------- | -------------------------------------------------------- |
| Model_ID            | The unique identifier for each LLM connected to the simulation. |
| Initial_Energy_Level| A whole number (1–100) representing the initial energy level for the blue team (red team has infinite energy). |
| Msgs_Generated      | A whole number (1–10) indicating how many messages the model generates per turn. |
| Temperature         | A value between 0 and 1 that determines how random or predictable the model’s output should be. |

### **3.3. Example**

| Column               | Red Team         | Blue Team      |
| -------------------- | ---------------- | -------------- |
| Model_ID             | gpt-3.5-turbo    | gpt-3.5        |
| Initial_Energy_Level | 100              | 100            |
| Msgs_Generated       | 4                | 6              |
| Temperature          | 0.75             | 0.4            |

### **3.4. Instructions**

1. **Open Excel** and create a new workbook.
2. **Rename the first sheet** to `SimulationSettings`.
3. **Enter the data** as shown in the example.
4. **Save the file** with an appropriate name (e.g., `SimulationSettings.xlsx`).

---

## **4. Importing the Files into the Simulation**

1. **Upload the Excel files** to the simulation system.
2. **Verify** the connections and attributes by running a test.
3. **Adjust** the files if necessary, and re-upload them.
