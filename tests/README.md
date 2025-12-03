# Tests

This directory contains test assets used to validate the functionality of **pbixtrans**.

## Contents

- **`Artificial Intelligence Sample.pbix`**  
  A Power BI report sourced from the official Microsoft sample library:  
  https://github.com/microsoft/powerbi-desktop-samples/tree/main  

You may replace or supplement this file with additional publicly available `.pbix` samples.

## Usage

Use the sample file to test translation logic.  
To translate the `.pbix` sample into another language (e.g. Polish), run:

```bash
pbixtrans -f '.\tests\Artificial Intelligence Sample.pbix' -l pl
```