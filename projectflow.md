main.py
Entry point of the project
Initializes the benchmarking process
Runs experiments on multiple datasets
Saves results and generates plots
main.py only controls the flow of execution and does not contain model or metric logic.

benchmark/runner.py
Core benchmarking controller
Streams datasets image by image (memory efficient)
Resizes images to multiple resolutions (2×2, 4×4, 8×8)
Executes all QIR models
Caches quantum circuits to avoid recomputation
Aggregates metrics at dataset level
This file ensures fair and consistent comparison across all models.

models/model.py
Contains all Quantum Image Representation (QIR) model implementations
Includes baseline models such as:

FRQI

NEQR

GQIR

MCQI

QPIE

QRMW, etc.
Implements SAQIR (proposed model)



metrics/evaluator.py
Computes scalable proxy metrics
Avoids full quantum state simulation
Extracts circuit properties such as:
Qubit count
Gate count
Circuit depth
Encoding time

Estimates:
Noise robustness
Reconstruction accuracy
Proxy metrics allow fast and scalable evaluation.

metrics/plots.py
Reads benchmark results from CSV
Generates comparison graphs automatically
Saves plots in results/graphs/
This file is used for visual analysis and comparison.

datasets/loader.py
Handles dataset access
Streams images one by one instead of loading the full dataset
Performs resizing and preprocessing
This design ensures low memory usage and scalability.


🔄 Execution Flow (How the Program Runs)

main.py starts execution
BenchmarkRunner is initialized
Each dataset is streamed image-by-image
Each image is resized to multiple resolutions
Each QIR model encodes the image into a quantum circuit
Proxy metrics are evaluated
Metrics are aggregated 
Results are saved as CSV
Comparison graphs are generated

📊 Datasets Used
MNIST (handwritten digits)
SAR images
Brain tumor images
Each dataset is evaluated independently to ensure fair comparison.

📈 Evaluation Metrics 

The project uses proxy metrics such as:

Qubit Count

Gate Count

Circuit Depth

Encoding Time  etc;

These metrics are:
Fast to compute
Scalable to large datasets


Benchmarking Framework
A structured system that compares multiple models fairly using the same datasets, resolutions, and metrics.

Scalable Proxy Metrics
Fast approximate measurements used instead of expensive quantum simulations, allowing experiments to scale efficiently.


🔬 SAQIR: Structure-Aware Quantum Image Representation

SAQIR is a quantum image representation method that uses the structure of the image to decide how many qubits are needed.

Instead of treating all image regions equally, SAQIR:
Gives more qubits to complex regions
Gives fewer qubits to simple regions

This makes the representation:

More efficient

More noise-robust

More suitable for NISQ devices

❌ Limitations of Traditional QIR Models

Most traditional QIR models:

Allocate fixed qubits for the entire image
Ignore whether a region is simple or complex
Waste qubits on flat or uniform regions

This results in:
High qubit count
Deep circuits


SAQIR – Key Idea
Divides the image into blocks
Computes entropy for each block
Allocates qubits adaptively based on image structure
Builds a single valid quantum circuit
This makes SAQIR structure-aware and resource-efficient.

👉 SAQIR solves this problem by being structure-aware.

📊 What is Entropy in SAQIR?
Entropy measures how much information or variation exists in an image region.

Entropy Calculation Steps:
The image is divided into small blocks (e.g., 4×4 pixels)

For each block:
Pixel values are collected
A histogram of intensities is created
Shannon entropy is computed
Conceptually:
More pixel variation → higher entropy
Less pixel variation → lower entropy

⚙️ SAQIR Circuit Construction
After deciding qubits per block:

Total qubits = sum of block-wise allocations

A single valid quantum circuit is created

SAQIR builds one valid quantum circuit while preserving region-wise structure.







 | **Technique**             | **Core Encoding Equation / Model**          | **What It Does**                                                           | **Main Limitation**                                      | **How SAQIR Solves It**                                                  |
| ------------------------- | ------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------ |
| **FRQI**                  | |I⟩ = (1/2ⁿ) Σₓ |x⟩ (cos θₓ|0⟩ + sin θₓ|1⟩) | Encodes pixel position in basis states and intensity in one rotation qubit | Single intensity qubit → low precision; uniform encoding | SAQIR allocates more qubits only to complex regions, improving precision |
| **NEQR**                  | |I⟩ = (1/2ⁿ) Σₓ |x⟩|b₀b₁…bₖ⟩                | Binary encoding of pixel intensities                                       | Very high qubit count; poor NISQ scalability             | SAQIR avoids binary encoding in low-entropy regions                      |
| **GQIR**                  | |I⟩ = Σₓ,ᵧ cₓᵧ |x⟩|y⟩                       | Generalized coordinate-based encoding                                      | Fixed qubit grid regardless of image content             | SAQIR adapts qubits based on image structure                             |
| **MCQI**                  | |I⟩ = Σₓ (R,G,B)ₓ ⊗ |x⟩                     | Multi-channel (RGB) quantum image encoding                                 | Gate-heavy, deep circuits                                | SAQIR reduces unnecessary gates in simple regions                        |
| **QdFRQI**                | |I⟩ = Σₓ (cos θₓ|00⟩ + sin θₓ|11⟩)          | Improves FRQI intensity precision                                          | Increased gate count and circuit depth                   | SAQIR achieves efficiency without duplicating intensity qubits           |
| **DCT-EFRQI**             | |I⟩ = Σₖ DCT(Iₖ)|k⟩                         | Frequency-domain quantum image encoding                                    | Transform overhead + uniform allocation                  | SAQIR works directly in spatial domain with adaptivity                   |
| **QPIE**                  | |I⟩ = Σₓ αₓ|x⟩                              | Compact pixel-intensity encoding                                           | Still globally fixed representation                      | SAQIR assigns resources region-wise                                      |
| **TNR** (Threshold-based) | |I⟩ = Σₓ f(Iₓ > τ)|x⟩                       | Encodes only significant pixels                                            | Loses fine-grained details                               | SAQIR preserves detail in high-entropy regions                           |
| **INQR**                  | |I⟩ = Σₓ |x⟩|Iₓ⟩                            | Integer-based exact representation                                         | High memory and qubit cost                               | SAQIR trades exactness for efficiency adaptively                         |
| **QRMW**                  | |I⟩ = Σₓ,ᵧ |x⟩|y⟩|Iₓᵧ⟩                      | Full matrix-wise image encoding                                            | Very high qubit requirement                              | SAQIR avoids full matrix encoding unless needed                          |
| **🧠 SAQIR (Proposed)**   | Q_total = Σᵢ f(Hᵢ), where Hᵢ = −Σ p log₂ p  | Structure-aware adaptive encoding using entropy                            | —                                                        | Efficient, noise-robust, NISQ-ready                                      |




| **Metric Name**                   | **What it Represents**                              | **How It Is Computed (Proxy / Logic)** | **Example Value** | **What This Value Means**              |
| --------------------------------- | --------------------------------------------------- | -------------------------------------- | ----------------- | -------------------------------------- |
| **Qubit_Count**                   | Total number of qubits required to encode the image | Directly read from the quantum circuit | `3`               | Very hardware-efficient representation |
| **Gate_Count**                    | Total quantum gates used in the circuit             | `qc.size()`                            | `5`, `10`, `23`   | Lower = fewer operations, less noise   |
| **Circuit_Depth**                 | Approximate sequential depth of the circuit         | `Gate_Count / Qubit_Count`             | `2`               | Shallow circuit, NISQ-friendly         |
| **Encoding_Time_ms**              | Classical time to construct/inspect circuit         | Measured using system timer            | `0.02 ms`         | Fast encoding overhead                 |
| **Gate_Fidelity_Impact**          | Impact of gate errors                               | `1 / (1 + Gate_Count)`                 | `0.125`           | Higher value = fewer gate errors       |
| **Noise_Robustness**              | Resistance to noise & decoherence                   | `1 / (1 + Circuit_Depth)`              | `0.333`           | Moderate noise tolerance               |
| **Reconstruction_Accuracy**       | Estimated ability to reconstruct image              | `1 / (1 + Qubits / Pixels)`            | `0.67`            | Good representation quality            |
| **Pixel_Accuracy**                | Fidelity at pixel-level detail                      | `1 / (1 + Gates / Pixels)`             | `0.44`            | Moderate pixel preservation            |
| **Information_Loss**              | Amount of information lost                          | `1 − Reconstruction_Accuracy`          | `0.33`            | Lower is better                        |
| **Scalability_Image_Size**        | Growth trend w.r.t image size                       | `log2(image_size)`                     | `2`, `4`, `6`     | Higher = larger resolution             |
| **Scalability_Image_Count**       | Scalability w.r.t dataset size                      | `1 / image_size`                       | `0.125`           | Smaller = harder to scale              |
| **Memory_Efficiency**             | Pixels encoded per qubit                            | `image_size / qubits`                  | `2.0`             | Higher = better compression            |
| **Transformation_Supportability** | Support for image operations                        | Fixed qualitative score                | `7`               | Neutral transformation support         |
| **NISQ_Suitability**              | Suitability for NISQ devices                        | `10 / (1 + Circuit_Depth)`             | `3.33`            | Moderately NISQ-feasible               |

