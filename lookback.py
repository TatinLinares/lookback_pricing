import numpy as np

def find_min(minimums, minimum):
    #Precondition: minimums is sorted
        low = 0
        high = len(minimums) - 1
        while low <= high:
            mid = (low + high) // 2
            if abs(minimums[mid][0] - minimum) < 0.0000001:
                return minimums[mid][1]
            elif minimums[mid][0] < minimum:
                low = mid + 1
            else:
                high = mid - 1
        return None

def americanPutLookBack(S0, K, r, sigma, T, N):
    dt = T / N # Time step
    u = np.exp(sigma * np.sqrt(dt)) # Up factor
    d = 1 / u # Down factor
    p = (np.exp(r * dt) - d) / (u - d) # Risk neutral probability
    q = 1-p
    disc = np.exp(-r*dt) # Discount factor

    S = np.zeros((N + 1), object) # Stock prices
    S[0] = [S0] # Initial stock price
    for i in range(1, N + 1):
        S[i] = [S[i - 1][0] * d] # Down movement
        for j in range(1, i + 1):
            S[i].append(S[i - 1][j - 1] * u) # Up movement

    minimums = np.zeros((N + 1), object) 
    minimums[0] = [[S0]]

    for i in range(1, N + 1):
        minimums[i] = []
        for j in range(0, i + 1):
            minimums_parent_up = minimums[i-1][j-1] if j-1 >= 0 else []
            minimums_parent_down = minimums[i-1][j] if j < i else []
            new_minimumsls =  []
            for minimum in minimums_parent_up + minimums_parent_down:
                if minimum < S[i][j]:
                    if minimum not in new_minimumsls:
                        new_minimumsls.append(minimum)
                else:
                    if S[i][j] not in new_minimumsls:
                        new_minimumsls.append(S[i][j])  
            minimums[i].append(new_minimumsls)

    for i in range(N + 1):
        for j in range(len(minimums[N][i])):
            minimums[N][i][j] = (minimums[N][i][j], K - minimums[N][i][j])

    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            for k in range(len(minimums[i][j])):
                    minimum = minimums[i][j][k]
                    esperar_up = find_min(minimums[i+1][j+1], minimum )  
                    esperar_down = find_min(minimums[i+1][j], min( S[i][j] * d, minimum ) ) 
                    esperar =  disc * (p * esperar_up + q * esperar_down)
                    minimums[i][j][k] = (minimum, max(K - minimum, esperar))

    print(f"Option price in t = 0 with {N} steps: {minimums[0][0][0][1]}")
    return minimums[0][0][0][1]


def main():
    print("American put lookback option, Strike = 90")
    americanPutLookBack(S0=100, K=90, r=0.1, sigma=0.4, T=1, N=20)
    americanPutLookBack(S0=100, K=90, r=0.1, sigma=0.4, T=1, N=30)
    americanPutLookBack(S0=100, K=90, r=0.1, sigma=0.4, T=1, N=40)
    print("American put lookback option, Strike = 100")
    americanPutLookBack(S0=100, K=100, r=0.1, sigma=0.4, T=1, N=20)
    americanPutLookBack(S0=100, K=100, r=0.1, sigma=0.4, T=1, N=30)
    americanPutLookBack(S0=100, K=100, r=0.1, sigma=0.4, T=1, N=40)
    print("American put lookback option, Strike = 110")
    americanPutLookBack(S0=100, K=110, r=0.1, sigma=0.4, T=1, N=20)
    americanPutLookBack(S0=100, K=110, r=0.1, sigma=0.4, T=1, N=30)
    americanPutLookBack(S0=100, K=110, r=0.1, sigma=0.4, T=1, N=40)


if __name__ == "__main__":
    main()