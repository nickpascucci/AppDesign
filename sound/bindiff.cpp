#include <iostream>
#include <fstream>
#include <iomanip>

using namespace std;

// Read unsigned char (byte)
unsigned char readByte(ifstream &thisFile){
char buffer;
thisFile.get(buffer);
return (unsigned char)buffer;
}

int main(int argc, char** argv)
{
ifstream binFileA(argv[1]);
ifstream binFileB(argv[2]);

int offset = 0;
unsigned char byteA;
unsigned char byteB;

cout << hex;

while(!binFileA.eof() && !binFileB.eof())
{
// Display file A
for(int i=0; i<6; i++)
{
byteA = readByte(binFileA);
cout << setw(3) << (int)byteA << " ";
}

cout << "| |";

// Display both files with "__" as difference
binFileA.seekg(-6, ios::cur);
for(int i=0; i<6; i++)
{
byteA = readByte(binFileA);
byteB = readByte(binFileB);
if(byteA != byteB){
cout << " __ ";
}
else
{
cout << setw(3) << (int)byteA << " ";
}
}

cout << "| |";

// Display file B
binFileB.seekg(-6, ios::cur);
for(int i=0; i<6; i++)
{
byteB = readByte(binFileB);
cout << setw(3) << (int)byteB << " ";
}

cout << endl;
}

binFileB.close();
binFileB.close();
}
