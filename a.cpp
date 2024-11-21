#include <iostream>
#define MAX 10001 // 1 <= n <= 10000

using namespace std; //

int main(){
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int n; // 1 <= n <= 10000
    cin >> n; // input n

    int arr[MAX]; // 포도주 양
    int dp[MAX]; // dp[i] = i번째 포도주까지 마셨을 때 최대 양

    for(int i = 1 ; i <= n ; i++){ // 포도주 양 입력
        cin >> arr[i]; // input arr[i]
    }

    dp[0] = arr[0] = 0; // 0번째 포도주는 없다고 가정
    dp[1] = arr[1]; // 1번째 포도주는 1번째 포도주만 마신다고 가정
    dp[2] = arr[1] + arr[2]; // 2번째 포도주는 1번째와 2번째 포도주를 마신다고 가정

    for(int i = 3; i <=n ; i++){ // 3번째 포도주부터는 3가지 경우를 고려한다.
    // 1. i-1번째 포도주를 마시지 않는 경우
    // 2. i-2번째 포도주를 마시지 않는 경우
    // 3. i-3번째 포도주를 마시지 않는 경우
    //  3가지 경우 중 최대값을 dp[i]에 저장한다.
        dp[i] = max(dp[i-3] + arr[i-1] + arr[i], max(dp[i-2] + arr[i], dp[i-1]));
    }
    
    cout << dp[n] << '\n';
    return 0;
}