#include <bits/stdc++.h>
#define forn(i, a, n) for(int i = a; i < n; i++)
using namespace std;
int main() {
  //freopen("input.txt", "r", stdin); freopen("output.txt", "w", stdout);"
  int n; scanf("%d", &n);
  int current = 0;
  int arr[n] = { current };
  forn(i, 0, n-1) {
    int value; scanf("%d", &value);
    current = value ^ current;
    arr[i+1] = current;
  }
  forn(d, 0, 30) {
    int n_ones = 0;
    forn(i, 0, n) {
      n_ones += ((arr[i] & (1 << d)) > 0);
    }
    // can make the set smaller keeping pairwise xor by flipping all d-th bits
    if (n_ones > n/2) {
      forn(i, 0, n) {
        arr[i] ^= (1 << d);
      }
    }
  }
  forn(i, 0, n) printf("%d ", arr[i]);
  printf("\n");
}
