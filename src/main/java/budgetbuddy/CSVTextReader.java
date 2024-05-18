package budgetbuddy;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.StringReader;

public class CSVTextReader {
	DataParser dp = new DataParser();
	CSVFileWriter fw = new CSVFileWriter();
	
	
	public void CSVReader(File file) {
		BufferedReader reader = null;
		String line = "";
		String[] fileRow = new String[5];
		String regex = "^[0-3]?[0-9]/[0-3]?[0-9]/(?:[0-9]{2})?[0-9]{2}$";

		
		try {
			reader = new BufferedReader(new FileReader(file));
			while((line = reader.readLine()) != null) {
				fileRow = dp.parseInputToArray(line);
				if ((fileRow[0].matches(regex))) {
					fw.writeToCSVFile(fileRow);   
				}
			}
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
			try {
				reader.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	
	}
	
	public void CSVReaderFromImage(String imageLines) {
		BufferedReader reader = null;
		String line = "";
		String[] fileRow = new String[5];
		String regex = "^[0-3]?[0-9]/[0-3]?[0-9]/(?:[0-9]{2})?[0-9]{2}$";

		
		try {
			reader = new BufferedReader(new StringReader(imageLines));
			while((line = reader.readLine()) != null) {
				fileRow = dp.parseInputToArray(line);
				if ((fileRow[0].matches(regex))) {
					fw.writeToCSVFile(fileRow);   
				}
			}
		} catch(Exception e) {
			e.printStackTrace();
		} finally {
			try {
				reader.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	
	}
	
}
