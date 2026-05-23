# SubBrute

A fast and efficient subdomain enumeration tool using brute-force with a wordlist.

## Features
- Concurrent DNS resolution for speed
- Simple command-line interface
- Customizable wordlist
- Outputs valid subdomains with their IP addresses

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SubBrute.git
   cd SubBrute
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
```bash
python subbrute.py -d example.com -w wordlist.txt
```

## Wordlist
The wordlist should contain one subdomain prefix per line (e.g., www, mail, ftp, admin, etc.).

## Example
```bash
python subbrute.py -d google.com -w wordlist.txt
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.