package budgetbuddy;

import java.io.File;

import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;

public class OCRImageText {
	public String ImageToText(File file) {
		Tesseract tesseract = new Tesseract();
		String result = "";
		
	    try {
	    	//path of the tess data folder
	    	tesseract.setDatapath("D:\\Projects\\Tess4J\\tessdata");
	    	
	        // Perform OCR on the image
	        result = tesseract.doOCR(file);
	    } catch (TesseractException e) {
	        System.err.println(e.getMessage());
	    }
	    return result;
	}
}
