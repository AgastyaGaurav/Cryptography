#include <iostream>
#include <vector>
#include <string>
#include <cctype>

using namespace std;

// Convert char to number (A=0..Z=25)
int ctoval(char c) { return toupper(c) - 'A'; }

// Convert number to char
char valtoc(int v) { return (char)(v + 'A'); }

// Compute determinant inverse mod 26
int modInverse(int det) {
    det = (det % 26 + 26) % 26;
    for(int x = 1; x < 26; x++)
        if((det * x) % 26 == 1)
            return x;
    return -1;
}

// Convert two words into 2×2 key matrix
vector<vector<int>> buildKeyMatrix(string w1, string w2) {
    string key = "";
    for(char c : w1) if(isalpha(c)) key += toupper(c);
    for(char c : w2) if(isalpha(c)) key += toupper(c);

    if(key.size() < 4) {
        cout << "Key must contain at least 4 letters!" << endl;
        exit(1);
    }

    vector<vector<int>> K(2, vector<int>(2));
    K[0][0] = ctoval(key[0]);
    K[0][1] = ctoval(key[1]);
    K[1][0] = ctoval(key[2]);
    K[1][1] = ctoval(key[3]);

    return K;
}

// Encrypt using Hill Cipher
string hillEncrypt(string plaintext, vector<vector<int>> K) {
    string p = "";
    for(char c : plaintext) if(isalpha(c)) p += toupper(c);

    // pad if odd number of letters
    if(p.size() % 2 == 1) p += 'X';

    string cipher = "";
    for(int i = 0; i < p.size(); i += 2) {
        int x1 = ctoval(p[i]);
        int x2 = ctoval(p[i+1]);

        int y1 = (K[0][0]*x1 + K[0][1]*x2) % 26;
        int y2 = (K[1][0]*x1 + K[1][1]*x2) % 26;

        cipher += valtoc(y1);
        cipher += valtoc(y2);
    }
    return cipher;
}

// MAIN
int main() {
    string word1, word2, plaintext;

    cout << "Enter Key Word 1: ";
    cin >> word1;

    cout << "Enter Key Word 2: ";
    cin >> word2;

    cout << "Enter Plaintext: ";
    cin.ignore();
    getline(cin, plaintext);

    // Build key matrix
    vector<vector<int>> K = buildKeyMatrix(word1, word2);

    cout << "\nKey Matrix (2x2):\n";
    cout << K[0][0] << " " << K[0][1] << endl;
    cout << K[1][0] << " " << K[1][1] << endl;

    // Encrypt
    string encrypted = hillEncrypt(plaintext, K);

    cout << "\nEncrypted Text: " << encrypted << endl;

    return 0;
}
