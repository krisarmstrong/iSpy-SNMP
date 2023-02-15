# iSpy SNMP

## Description

This program is a multithreaded SNMP reader that retrieves interface information
via the SNMP interface MIB for all devices within a given subnet. It is written in
Python 3.11, uses asyncio for improved performance, and adheres to PEP8 conventions for
naming variables and functions, with appropriate docstrings and comments to explain
the purpose and functionality of each component of the program.

## Author

Kris Armstrong

## License

This program is licensed under the Apache 2.0 License.

## Usage

To use the program, simply run it in a Python 3.11 environment on the command line. The
program will prompt you for the IP subnet to retrieve interface information for, as well
as the SNMP community string to use for authentication. The program will then retrieve the
interface information via SNMP using the interface MIB for all devices within the specified
subnet and print the information to the console.

## Contributing

If you would like to contribute to this program, please feel free to submit a pull request
with any bug fixes or feature enhancements. Before submitting a pull request, please ensure
that your changes are in compliance with the PEP 8 coding style guide and the existing codebase.

## Issues

If you encounter any issues or bugs with this program, please submit an issue on the GitHub repository.

## Acknowledgments

This program was inspired by the benefits of using asyncio for improved performance and the usefulness of the SNMP interface MIB for network monitoring.

## Future Development

- Integration with other Python libraries for expanded functionality
- GUI for easy-to-use interface
- Ability to output interface information to a file

## Release History

- 0.1.0
  - Initial release

