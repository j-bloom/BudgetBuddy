package budgetbuddy;

import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JLayeredPane;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JLabel;
import java.awt.Font;
import java.awt.CardLayout;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JTextField;
import com.toedter.calendar.JDateChooser;
import javax.swing.JTable;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Date;
import java.awt.event.ActionEvent;
import javax.swing.table.DefaultTableModel;
import javax.swing.border.BevelBorder;
import javax.swing.JScrollPane;

public class MainPage extends JFrame {

    DataParser dataParser = new DataParser();
    CSVFileWriter writer = new CSVFileWriter();
    CSVTextReader CSVTextreader = new CSVTextReader();
    OCRImageText imageText = new OCRImageText();
	
	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private JDateChooser dateChooser;
	private JTextField storeField;
	private JTextField descriptionField;
	private JTextField categoryField;
	private JTextField priceField;
	private JTable table;
	private JLayeredPane layeredPane;
	private JPanel home;
	private JPanel manualEntry;
	private JPanel mergeCSV;
	private JPanel importImage;
	

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MainPage frame = new MainPage();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	
	public void switchPanels(JPanel panel) {
		layeredPane.removeAll();
		layeredPane.add(panel);
		layeredPane.repaint();
		layeredPane.revalidate();
	}

	/**
	 * Create the frame.
	 */
	public MainPage() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 800, 550);
		
		JMenuBar menuBar = new JMenuBar();
		setJMenuBar(menuBar);
		
		JMenu navigateMenu = new JMenu("Navigate");
		menuBar.add(navigateMenu);
		
		JMenuItem manualMenuItem = new JMenuItem("Manual Entry");
		manualMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				switchPanels(manualEntry);
				addRowData();
			}
		});
		
		JMenuItem homeMenuItem = new JMenuItem("Home");
		homeMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				switchPanels(home);
			}
		});
		navigateMenu.add(homeMenuItem);
		navigateMenu.add(manualMenuItem);
		
		JMenuItem mergeMenuItem = new JMenuItem("Merge CSVs");
		mergeMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				switchPanels(mergeCSV);
			}
		});
		navigateMenu.add(mergeMenuItem);
		
		JMenuItem importMenuItem = new JMenuItem("Import Image");
		importMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				switchPanels(importImage);
			}
		});
		navigateMenu.add(importMenuItem);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));

		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		layeredPane = new JLayeredPane();
		layeredPane.setBounds(10, 10, 764, 468);
		contentPane.add(layeredPane);
		layeredPane.setLayout(new CardLayout(0, 0));
		
		home = new JPanel();
		layeredPane.add(home, "name_13957023892900");
		home.setLayout(null);
		
		//Home Page
		JLabel welcomeLabel = new JLabel("Welcome To Your Budget Buddy!");
		welcomeLabel.setBounds(221, 5, 322, 27);
		welcomeLabel.setFont(new Font("Tahoma", Font.PLAIN, 22));
		home.add(welcomeLabel);
		
		JLabel logoLabel = new JLabel("");
		logoLabel.setIcon(new ImageIcon("..\\budgetbuddy\\images\\budgetBuddyLogo.png"));
		logoLabel.setFont(new Font("Tahoma", Font.PLAIN, 22));
		logoLabel.setBounds(106, 60, 552, 397);
		home.add(logoLabel);
		
//		TODO: Add functionality to create a new file
//		JButton addButton = new JButton("");
//		addButton.setIcon(new ImageIcon("..\\budgetbuddy\\images\\add-icon.png"));
//		addButton.setFocusable(false);
//		addButton.setFont(new Font("Tahoma", Font.BOLD, 16));
//		addButton.setBounds(712, 11, 42, 35);
//		home.add(addButton);
		
		//Manual Entry Page Elements
		manualEntry = new JPanel();
		layeredPane.add(manualEntry, "name_13957032674600");
		manualEntry.setLayout(null);
		
		//Manual Entry Labels
		JLabel dateLabel = new JLabel("Date:");
		dateLabel.setFont(new Font("Tahoma", Font.PLAIN, 16));
		dateLabel.setBounds(25, 50, 100, 25);
		manualEntry.add(dateLabel);
		
		JLabel storeLabel = new JLabel("Store:");
		storeLabel.setFont(new Font("Tahoma", Font.PLAIN, 16));
		storeLabel.setBounds(25, 100, 100, 25);
		manualEntry.add(storeLabel);
		
		JLabel descriptionLabel = new JLabel("Description:");
		descriptionLabel.setFont(new Font("Tahoma", Font.PLAIN, 16));
		descriptionLabel.setBounds(25, 150, 100, 25);
		manualEntry.add(descriptionLabel);
		
		JLabel lblCategory = new JLabel("Category:");
		lblCategory.setFont(new Font("Tahoma", Font.PLAIN, 16));
		lblCategory.setBounds(25, 200, 100, 25);
		manualEntry.add(lblCategory);
		
		JLabel priceLabel = new JLabel("Price:");
		priceLabel.setFont(new Font("Tahoma", Font.PLAIN, 16));
		priceLabel.setBounds(25, 250, 100, 25);
		manualEntry.add(priceLabel);
		
		//Manual Entry Text Fields
		dateChooser = new JDateChooser();
		dateChooser.setBounds(115, 50, 200, 25);
		manualEntry.add(dateChooser);
		
		storeField = new JTextField();
		storeField.setBounds(115, 100, 200, 25);
		manualEntry.add(storeField);
		storeField.setColumns(10);
		
		descriptionField = new JTextField();
		descriptionField.setColumns(10);
		descriptionField.setBounds(115, 150, 200, 25);
		manualEntry.add(descriptionField);
		
		categoryField = new JTextField();
		categoryField.setColumns(10);
		categoryField.setBounds(115, 200, 200, 25);
		manualEntry.add(categoryField);
		
		priceField = new JTextField();
		priceField.setColumns(10);
		priceField.setBounds(115, 250, 200, 25);
		manualEntry.add(priceField);
		
		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setBounds(325, 50, 430, 329);
		manualEntry.add(scrollPane);
		
		table = new JTable();
		scrollPane.setViewportView(table);
		table.setBorder(new BevelBorder(BevelBorder.LOWERED, null, null, null, null));
		table.setFont(new Font("Tahoma", Font.PLAIN, 12));
		table.setModel(new DefaultTableModel(
			new Object[][] {
			},
			new String[] {
				"Date", "Store", "Price"
			}
		));
		table.setColumnSelectionAllowed(true);
		
		//Manual Entry Preview 
		//Displays a preview of the current CSV File
		JLabel previewCSV = new JLabel("File Preview");
		previewCSV.setFont(new Font("Tahoma", Font.PLAIN, 16));
		previewCSV.setBounds(496, 14, 89, 25);
		manualEntry.add(previewCSV);
		
		JButton saveButton = new JButton("Save");
		saveButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
		        if(e.getSource()==saveButton) {
		        	Date getDate = dateChooser.getDate();
		        	String date = String.format("%1$tm/%1$td/%1$tY",getDate); 
		            String store = storeField.getText();
		            String description = descriptionField.getText();
		            String category = categoryField.getText();
		            String price = priceField.getText();
		            System.out.println(date);
		            SetFormDataToArray(date, store, description, category, price);
		        }
			}
		});
		

		saveButton.setBounds(115, 386, 75, 25);
		manualEntry.add(saveButton);
		
		JButton resetButton = new JButton("Reset");
		resetButton.setBounds(240, 386, 75, 25);
		manualEntry.add(resetButton);
		
		JButton refreshButton = new JButton("Refresh Table");
		refreshButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				addRowData();
			}
		});
		refreshButton.setBounds(483, 387, 130, 23);
		manualEntry.add(refreshButton);
		
		//Merge CSV Page
		mergeCSV = new JPanel();
		layeredPane.add(mergeCSV, "name_13957041795200");
		mergeCSV.setLayout(null);
		
		JLabel mergePageLabel = new JLabel("Merge CSV Into Current File");
		mergePageLabel.setBounds(255, 5, 254, 35);
		mergePageLabel.setFont(new Font("Tahoma", Font.PLAIN, 20));
		mergeCSV.add(mergePageLabel);
		
		JLabel mergeSelectFileLabel = new JLabel("Select a file to Merge");
		mergeSelectFileLabel.setFont(new Font("Tahoma", Font.PLAIN, 16));
		mergeSelectFileLabel.setBounds(308, 195, 147, 20);
		mergeCSV.add(mergeSelectFileLabel);
		
		JButton mergeSelectButton = new JButton("Select File");
		mergeSelectButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			   	if(e.getSource()==mergeSelectButton) {
		            JFileChooser fileChooser = new JFileChooser();
		            fileChooser.setCurrentDirectory(new File("C:\\Users\\J\\Downloads"));
		            int response = fileChooser.showOpenDialog(null);
		            if(response == JFileChooser.APPROVE_OPTION) {
		         	   File file1 = new File(fileChooser.getSelectedFile().getAbsolutePath());
		         	   try {
		         		  CSVTextreader.CSVReader(file1);
		         	   } catch(Exception e1) {
		         		   e1.printStackTrace();
		         	   }
		            }
			   	}
			}
		});
		mergeSelectButton.setFont(new Font("Tahoma", Font.PLAIN, 12));
		mergeSelectButton.setBounds(337, 226, 89, 23);
		mergeCSV.add(mergeSelectButton);
		
		JLabel mergeInformationLabel = new JLabel("* Files must be in CSV Format");
		mergeInformationLabel.setFont(new Font("Tahoma", Font.ITALIC, 11));
		mergeInformationLabel.setBounds(10, 443, 147, 14);
		mergeCSV.add(mergeInformationLabel);
		
		//Import CSV Page 
		importImage = new JPanel();
		layeredPane.add(importImage, "name_13957050774500");
		importImage.setLayout(null);
		
		JLabel importPageLabel = new JLabel("Import Screenshot of Budget");
		importPageLabel.setBounds(254, 5, 256, 35);
		importPageLabel.setFont(new Font("Tahoma", Font.PLAIN, 20));
		importImage.add(importPageLabel);

		JLabel importSelectFileLabel = new JLabel("Select a file to Import");
		importSelectFileLabel.setFont(new Font("Tahoma", Font.PLAIN, 16));
		importSelectFileLabel.setBounds(305, 195, 153, 20);
		importImage.add(importSelectFileLabel);
		
		JButton importSelectButton = new JButton("Select File");
		importSelectButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
		        if(e.getSource()==importSelectButton) {
		            JFileChooser fileChooser = new JFileChooser();
		            fileChooser.setCurrentDirectory(new File("C:\\Users\\J\\Downloads"));
		            int response = fileChooser.showOpenDialog(null);
		            if(response == JFileChooser.APPROVE_OPTION) {
		         	   File file = new File(fileChooser.getSelectedFile().getAbsolutePath());
		         	   String data = imageText.ImageToText(file);
		         	   try {
		         		CSVTextreader.CSVReaderFromImage(data);
		         	   } catch(Exception e1) {
		         		   e1.printStackTrace();
		         	   }
		            }
		        }
			}
		});
		importSelectButton.setFont(new Font("Tahoma", Font.PLAIN, 12));
		importSelectButton.setBounds(337, 226, 89, 23);
		importImage.add(importSelectButton);
	}
	
	private void SetFormDataToArray(String date, String store, String description, String category, String price) {

        String formInformation = date + "," + store + "," + description + "," + category + "," + price + ",";

        try {
            String[] data = new String[5];
            data = dataParser.parseInputToArray(formInformation);
            writer.writeToCSVFile(data);
            dateChooser.setCalendar(null);
            storeField.setText("");
            descriptionField.setText("");
            categoryField.setText("");
            priceField.setText("$");

        } catch(Exception e) {
            e.printStackTrace();
        }
    }
	
	public void addRowData() {
		BufferedReader reader = null;
		String line = "";
		String fileName = "monthly budget.csv";
		String regex = "^[0-3]?[0-9]/[0-3]?[0-9]/(?:[0-9]{2})?[0-9]{2}$";
		
		DefaultTableModel model = (DefaultTableModel)table.getModel();
		model.setRowCount(0);
		try {
			reader = new BufferedReader(new FileReader(fileName));
			while((line = reader.readLine()) != null) {
				String[] fileRow = dataParser.parseInputToArray(line);
				if ((fileRow[0].matches(regex)) && (fileRow.length >= 4)) {
					model.addRow(new Object[] {
						fileRow[0],  fileRow[1], fileRow[4]
					});
				}
			}
		} catch (Exception err) {
			err.printStackTrace();
	    } finally {
	        try {
	            if (reader != null) {
	                reader.close();
	            }
	        } catch (IOException e) {
	            e.printStackTrace();
	        }
	    }
	}
}
