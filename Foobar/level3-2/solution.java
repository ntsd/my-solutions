import java.math.BigInteger;

public class Solution {
    public static String solution(String x, String y) {
        BigInteger bigx = new BigInteger(x);
        BigInteger bigy = new BigInteger(y);

		if (x.equals("1")) {
			return bigy.subtract(BigInteger.ONE).toString();
		}
		if (y.equals("1")) {
			return bigx.subtract(BigInteger.ONE).toString();
		}

		if (bigx.mod(bigy) == BigInteger.ZERO || bigy.mod(bigx) == BigInteger.ZERO) {
			return "impossible";
		}

		BigInteger minBomb = bigx.min(bigy);
    	BigInteger maxBomb = bigx.max(bigy);

		return (maxBomb.divide(minBomb).add(minBomb).subtract(BigInteger.ONE)).toString();
    }
}
