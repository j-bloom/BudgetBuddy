package budgetbuddy;

public class DataParser {
	 public String[] parseInputToArray(String input) {
	        // Splitting the input string by commas
	        String[] tokens = input.split(",");

	        // Trimming whitespace from each part
	        for (int i = 0; i < tokens.length; i++) {
	            tokens[i] = tokens[i].trim();
	        }

	        return tokens;
	    }
}
