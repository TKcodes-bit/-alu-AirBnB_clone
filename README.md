# alu-AirBnB_clone

## Descriptions
ALU AirBnB Project is a clone of the popular AirBnB platform, designed to provide a similar experience for users looking to rent or list properties.

## Features
- User authentication and authorization
- Property listing and searching
- Booking management
- Reviews and ratings
- Responsive design

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/TKcodes-bit/alu-AirBnB_clone
   ```
2. Navigate to the project directory:
   ```bash
   cd alu-AirBnB_clone
   ```
3. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

## Usage
Run the HBNB console:
```bash
./console.py
```
Basic commands:
- `create <ClassName>`: create an instance and print its id
- `show <ClassName> <id>`: print the instance
- `destroy <ClassName> <id>`: delete the instance
- `all [<ClassName>]`: show all instances (optionally filtered by class)
- `update <ClassName> <id> <attr_name> <attr_value>`: set attribute
Also supports dot notation, e.g. `BaseModel.all()`, `User.show(<id>)`, `Place.update(<id>, max_guest, 4)`.

## Project Structure
- `models/` - Core models and storage engine
- `console.py` - Command interpreter
- `tests/` - Unit tests

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Authors
- Paul Masamvu - (https://github.com/Paul-202425)
- Thomas Kweya - (https://github.com/TKcodes-bit)
