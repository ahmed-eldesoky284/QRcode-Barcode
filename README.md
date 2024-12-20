# QR Code and Barcode Generator

This Streamlit app allows you to generate **QR Codes** and **Barcodes** with customizable options. You can create QR codes with specific colors, backgrounds, and even add a logo in the center. Additionally, you can generate barcodes with a custom or random 12-digit number.

## Features

### QR Code Generator:
- **Customizable Color:** Choose the color for the QR code.
- **Customizable Background:** Select the background color for the QR code.
- **Logo Insertion:** Optionally, upload a logo to be placed in the center of the QR code.
- **Size of Logo:** Adjust the size of the logo as a percentage of the QR code.
- **Downloadable PNG:** Download the generated QR code as a PNG image.

### Barcode Generator:
- **Custom Barcode Number:** Enter a custom 12-digit barcode number.
- **Random Barcode Number:** If no number is entered, a random 12-digit barcode is generated.
- **Downloadable PNG:** Download the generated barcode as a PNG image.

## Requirements

To run this app, you need to have Python installed along with the following dependencies:
- `streamlit`
- `qrcode`
- `Pillow`
- `python-barcode`

You can install the necessary dependencies by running the following command:

```bash
pip install streamlit qrcode[pil] pillow python-barcode
```
## How to Use
1. Run the App:
After installing the dependencies, navigate to the project directory and run the following command to start the Streamlit app:
```bash
streamlit run app.py
```
2. Select the Code Type:
Choose between QR Code or Barcode from the dropdown menu.
3. For QR Code:
Enter the link or text to generate a QR code.
Customize the color and background of the QR code.
Optionally, upload a logo to be placed in the center of the QR code.
Adjust the size of the logo.
Once done, the QR code will be displayed, and you can download it.
4. For Barcode:
Enter a custom 12-digit barcode number or leave it blank to generate a random number.
The generated barcode will be displayed, and you can download it.

## Example Usage
- QR Code Example:
   - Input:  `https://www.example.com`
   - Custom Colors: Black text on a white background
   - Optional Logo: Upload an image to be placed in the center of the QR code.
- Barcode Example:
   - Input: `123456789012`
   - If no input is provided, a random barcode will be generated.
 
## Acknowledgments

`Streamlit`
`qrcode`
`Pillow`
`python-barcode`

## License
This project is licensed under the MIT License - see the LICENSE file for details.
