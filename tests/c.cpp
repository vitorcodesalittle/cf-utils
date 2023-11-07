#include <bits/stdc++.h>
#define forn(i, a, n) for(int i = a; i < n; i++)
using namespace std;
int sum_counter[5][46];
inline vector<int> get_digits(int n) {
  vector<int> digits;
  while (n > 9) {
    digits.push_back(n % 10);
    n /= 10;
  }
  digits.push_back(n%10);
  reverse(digits.begin(), digits.end());
  return digits;
}
int main() {
  //freopen("input.txt", "r", stdin); freopen("output.txt", "w", stdout);"
  int n; scanf("%d", &n);
  int arr[n];
  vector<vector<int>> digits(n);
  vector<int> digits_sum(n);
  forn(i, 0, n) {
    scanf("%d", arr + i);
    digits[i] = get_digits(arr[i]);
    for (int digit : digits[i]) digits_sum[i] += digit;
    sum_counter[digits[i].size()][digits_sum[i]] += 1;
  }
  long long total = 0;
  forn(i, 0, n) {
    if (digits[i].size() == 2) {
      total += sum_counter[2][digits_sum[i]];
    } else if (digits[i].size() == 4) {
      total += sum_counter[4][digits_sum[i]];
      total += sum_counter[2][digits_sum[i] - 2 * digits[i][0]];
      total += sum_counter[2][digits_sum[i] - 2 * digits[i][digits[i].size()-1]];
    } else if (digits[i].size() == 1) {
      total += sum_counter[1][digits_sum[i]];
    } else if (digits[i].size() == 3) {
      total += sum_counter[3][digits_sum[i]];
      total += sum_counter[1][digits_sum[i] - 2 * digits[i][0]];
      total += sum_counter[1][digits_sum[i] - 2 * digits[i][digits[i].size() - 1]];
    } else {
      total += sum_counter[5][digits_sum[i]];
      total += sum_counter[3][digits_sum[i] - 2 * digits[i][0]];
      total += sum_counter[3][digits_sum[i] - 2 * digits[i][digits[i].size() - 1]];
      total += sum_counter[1][digits_sum[i] - 2 * digits[i][0] - 2 * digits[i][1]];
      total += sum_counter[1][digits_sum[i] - 2 * digits[i][digits[i].size() - 1] - 2 * digits[i][digits[i].size() - 2]];
    }
  }
  printf("%lld\n", total);
}
