# Heat Exchanger Analysis and Design

This project provides tools for conducting an energy balance and designing a heat exchanger. The script allows users to input the chemical components of hot and cold fluids, calculate heat capacities, and perform heat transfer calculations.

## Project Overview

The primary objectives of this project are:
- **Energy Balance**: Calculate the input and output heat transferred by the fluids.
- **Heat Exchanger Design**: Determine the necessary heat load and evaluate heat exchanger performance using the Log Mean Temperature Difference (LMTD) method and the Effectiveness-NTU method.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nawwarad/heat-exchanger-analysis.git
   cd heat-exchanger-analysis
   ```
2. **Install dependencies**:
   Ensure you have Python installed, then install the required packages:
   ```bash
   pip install numpy chemicals ht
   ```

## Usage

1. **Run the script**:
   ```bash
   python heat-exchanger.py
   ```
2. **Input data**:
   - Enter the components of the cold and hot fluids when prompted.
   - Input temperatures for both the cold and hot fluids at their entry and exit points in Kelvin.

3. **Output**:
   - The script will output the calculated heat capacities, heat transferred, and heat load. It will also provide an analysis of the heat exchanger's performance.

## Bugs or Future Development

### Known Issues

- The current implementation does not divide the heat capacity by the molar weight of the species, which may lead to inaccurate calculations.

### Future Improvements

- Correct the calculation by dividing the heat capacity (`Q`) by the molar weight of the species.
- Enhance user input validation and error handling.
- Implement additional methods for heat exchanger analysis and design.
- Add a graphical user interface for easier interaction.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/nawwarad/process-engineering/blob/main/LICENSE) file for more details.
