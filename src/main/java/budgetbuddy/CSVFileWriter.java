package budgetbuddy;

import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;

public class CSVFileWriter {
	public void writeToCSVFile(String[] data) {
		String fileName = "monthly budget.csv";

		try {
			FileWriter fw = new FileWriter(fileName, true);
			for (String item : data) {
				fw.append(item);
	            fw.append(",");
			}
	        fw.append("\n");
	        fw.flush();
	        fw.close();
	        } catch (FileNotFoundException e) {
	            System.out.println("Error writing to file");
	            e.printStackTrace();
	        } catch (IOException e) {
	            System.out.println("An error occurred while writing to the CSV file.");
	            e.printStackTrace();
	        }
	    }

}