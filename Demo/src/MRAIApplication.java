import java.awt.KeyEventDispatcher;
import java.awt.KeyboardFocusManager;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;

public class MRAIApplication {

	static DemoWindow dm;
	static LeaderBoard lb;
	static NameWindow n;
	static MyThread thread;
	static MyTimer t;

	static String tempName = "";

	static int save_file_numbers = 0;
	
	int file_number = 7;
	static int file_count = 1;

	static List<String> names = new ArrayList<>();
	static List<Integer> totalImages = new ArrayList<>();
	static List<Float> accuracies = new ArrayList<>();

	/**
	 * @param args
	 */
	public static void main(String[] args) {

		// start UI
		// TODO startup the UI corresponding to the right mode?
		java.awt.EventQueue.invokeLater(new Runnable() {
			public void run() {

				names.add(0, "MR-AI");
				totalImages.add(0, 0);
				accuracies.add(0, (float) 0.0);

				dm = new DemoWindow();
				lb = new LeaderBoard();
				n = new NameWindow();
				n.setVisible(true);

				try {
					setCSV();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				dm.setVisible(true);
				dm.addKeyListener(new MyKeyListener(dm, t));

				// bot
				thread = new MyThread(dm);
				// thread.start();

				t = new MyTimer(thread, dm, lb);
				t.setVisible(true);
				dm.toFront();
				t.startBtn.setEnabled(false);
				n.toFront();
				t.startBtn.setEnabled(true);
			}
		});

	}

	public static void reset() {
		file_count++;
		if (file_count > 7) {
			file_count = 0;
		}
		dm = new DemoWindow();
		lb = new LeaderBoard();
		n = new NameWindow();

		try {
			setCSV();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		dm.setVisible(true);
		dm.addKeyListener(new MyKeyListener(dm, t));

		// bot
		thread = new MyThread(dm);
		// thread.start();

		t = new MyTimer(thread, dm, lb);
		t.setVisible(true);
		t.setEnabled(true);
		dm.toFront();
		try {
			writeFile();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public static void writeFile() throws IOException {
		FileWriter writer = new FileWriter("/Users/li-tigre/Desktop/scores/score" + Integer.toString(save_file_numbers) + ".txt");
		writer.write("Name\t images\t accuracy\n");
		for (int i = 0; i < names.size(); i++) {
			writer.write(names.get(i) + "\t" + totalImages.get(i) + "\t" + accuracies.get(i) + "\n");
		}

//		for (String str : arr) {
//			writer.write(str);
//		}
		save_file_numbers++;
		writer.close();
	}

	public static void setCSV() throws IOException {

		List<String> imageNames = new ArrayList<>();
		List<String> imageLabels = new ArrayList<>();
		List<String> botLabels = new ArrayList<>();

		// The name of the file to open.
		String fileName = "/Users/li-tigre/Desktop/MR_AI/Demo_game/random200_" + file_count + ".csv";
		String botFile = "/Users/li-tigre/Desktop/MR_AI/Demo_game/randomBot_" + file_count + ".csv";
		
		// This will reference one line at a time
		String line = null;

		try {
			// FileReader reads text files in the default encoding.
			FileReader fileReader = new FileReader(fileName);

			// Always wrap FileReader in BufferedReader.
			BufferedReader bufferedReader = new BufferedReader(fileReader);

			while ((line = bufferedReader.readLine()) != null) {
				String[] lines = line.split(",");
				System.out.println(lines);
				imageNames.add(lines[0]);
				imageLabels.add(lines[1]);
				// line = bufferedReader.readLine();
			}

			// Always close files.
			bufferedReader.close();
		} catch (FileNotFoundException ex) {
			System.out.println("Unable to open file '" + fileName + "'");
		}
		
		try {
			// FileReader reads text files in the default encoding.
			FileReader fileReader = new FileReader(botFile);

			// Always wrap FileReader in BufferedReader.
			BufferedReader bufferedReader = new BufferedReader(fileReader);

			while ((line = bufferedReader.readLine()) != null) {
				String[] lines = line.split(",");
//				System.out.println(lines);
//				imageNames.add(lines[0]);
				botLabels.add(lines[1]);
				// line = bufferedReader.readLine();
			}

			// Always close files.
			bufferedReader.close();
		} catch (FileNotFoundException ex) {
			System.out.println("Unable to open file '" + fileName + "'");
		}
		
		dm.setArrays(imageNames, imageLabels, botLabels);
		dm.l = imageLabels.size();
		dm.isFileSet = true;
		dm.refresh();

	}

	public static void newGame() {
		// TODO Auto-generated method stub
		n = new NameWindow();
		n.setVisible(true);
		n.toFront();
		lb.close();
	}

}

class MyKeyListener extends KeyAdapter {

	DemoWindow dm;
	MyTimer t;

	public MyKeyListener(DemoWindow d, MyTimer timer) {
		dm = d;
		t = timer;
	}

	public void keyPressed(KeyEvent evt) {
		if (dm.isPlaying) {

			dm.total_img++;

			if (evt.getKeyChar() == 'a') {
				// TODO: replace by left arrow --> meaning clear image --> 0
//				System.out.println(evt.getKeyCode());
				dm.checkImgHuman(dm.imgCount, "0");

				dm.imgCount++;
				dm.refresh();
			}
			if (evt.getKeyChar() == 'd') {
				// System.out.println("Check for key characters: " + evt.getKeyChar());

				dm.checkImgHuman(dm.imgCount, "1");
//				System.out.println(evt.getKeyCode());

				dm.imgCount++;
				// System.out.println(dm.imgCount);

				dm.refresh();
			}
			if (evt.getKeyCode() == KeyEvent.VK_HOME) {
				System.out.println("Check for key codes: " + evt.getKeyCode());
			}
		}

	}
}
