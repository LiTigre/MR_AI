import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import javax.imageio.ImageIO;
import javax.swing.GroupLayout;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.GroupLayout.Alignment;
import javax.swing.ImageIcon;
import javax.swing.border.EmptyBorder;

import javax.swing.JButton;
import javax.swing.LayoutStyle.ComponentPlacement;
import javax.swing.JRadioButton;
import javax.swing.JSplitPane;
import javax.swing.JLabel;
import java.awt.Font;
import java.awt.Image;
import java.awt.Color;
import java.awt.Dimension;

import javax.swing.JTextField;
import javax.swing.border.LineBorder;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;

public class DemoWindow extends JFrame {

	// main panel
	private JSplitPane split_pane;
	// left side
	private JPanel leftPanel;
	private JLabel leftLbl;
	private JLabel imgCountLeft;
	private JLabel imageLeft;

	private JLabel correctCountLeft;

	// right panel
	private JPanel rightPanel;
	private JLabel rightLbl;
	private JLabel imageRight;

	// image data
	static List<String> myImages;
	static List<String> myLabels;
	static List<String> botLabels;
	int total_img = 0; // size of myImages

	int l = 0;

	public static int imgCount = 0; // index of the current images and labels for human
	public static int imgCountAI = 0;

	boolean isFileSet = false;

	// game logic
	public static int correctCount = 0; // how many correct images the user identified
	public static int totalCount = 0; // how many images the user cleared

	public static int correctCountAI = 0;
	public static int totalCountAI = 0;
	private JLabel imgCountRight;
	private JLabel correctCountRight;

	public boolean isPlaying = false;
	private JButton btnNewButton;
	private JButton btnNoisy;

	/**
	 * Create the frame.
	 */
	public DemoWindow() {
		setTitle("Play Mode: Game number ");
		initialize();
		Random rand = new Random();

		imgCount = rand.nextInt(200);
		imgCountAI = imgCount;
		initComponents();
		refresh();
	}
	
	public void initialize() {
		imgCount = 0;
		imgCountAI = 0;
		isFileSet = false;
		correctCount = 0;
		totalCount = 0;
		correctCountAI = 0;
		totalCountAI = 0;
	}

	public void close() {
		this.setVisible(false);
		this.dispose();
	}

	public static void setArrays(List<String> images, List<String> labels, List<String> botLbl) {
		myImages = images;
		myLabels = labels;
		botLabels = botLbl;
		
	}

	public static void setError(String error) {
	}

	private void initComponents() {
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		this.setExtendedState(JFrame.MAXIMIZED_BOTH);
		this.setSize(1300, 750);
		this.setResizable(false);

		split_pane = new JSplitPane();
		split_pane.setBackground(Color.WHITE);
		split_pane.setSize(1300, 750);
		split_pane.setDividerSize(0);
		split_pane.setDividerLocation(640);
		split_pane.setOrientation(JSplitPane.HORIZONTAL_SPLIT);

		GroupLayout groupLayout = new GroupLayout(getContentPane());
		groupLayout.setHorizontalGroup(groupLayout.createParallelGroup(Alignment.LEADING)
				.addGroup(groupLayout.createSequentialGroup().addGap(3)
						.addComponent(split_pane, GroupLayout.DEFAULT_SIZE, 1291, Short.MAX_VALUE).addContainerGap()));
		groupLayout.setVerticalGroup(
				groupLayout.createParallelGroup(Alignment.LEADING).addGroup(groupLayout.createSequentialGroup()
						.addContainerGap().addComponent(split_pane, GroupLayout.DEFAULT_SIZE, 722, Short.MAX_VALUE)));

		leftPanel = new JPanel();
		leftPanel.setBorder(new LineBorder(new Color(0, 0, 0)));
		split_pane.setLeftComponent(leftPanel);

		leftLbl = new JLabel("YOU");
		leftLbl.setHorizontalAlignment(JLabel.CENTER);
		leftLbl.setFont(new Font("Lucida Grande", Font.BOLD, 28));

		imageLeft = new JLabel("");
		imageLeft.setHorizontalAlignment(JLabel.CENTER);
		imageLeft.setPreferredSize(new Dimension(400, 400));

		imgCountLeft = new JLabel("Image Count: 0");
		imgCountLeft.setFont(new Font("Lucida Grande", Font.PLAIN, 17));

		correctCountLeft = new JLabel("Correct Count: 0");
		correctCountLeft.setFont(new Font("Lucida Grande", Font.PLAIN, 17));
		
		btnNewButton = new JButton("Clean (A)");
		btnNewButton.setEnabled(false);
//		btnNewButton.addMouseListener(new MouseAdapter() {
//			@Override
//			public void mouseClicked(MouseEvent e) {
//				checkImgHuman(imgCount, "0");
//				imgCount++;
//				refresh();
//			}
//		});
//		btnNewButton.addActionListener(new ActionListener() {
//			public void actionPerformed(ActionEvent e) {
//				
//				
//			}
//			
//		});
		
		btnNoisy = new JButton("Noisy (D)");
		btnNoisy.setEnabled(false);
//		btnNoisy.addMouseListener(new MouseAdapter() {
//			@Override
//			public void mouseClicked(MouseEvent e) {
//				checkImgHuman(imgCount, "1");
//				imgCount++;
//				refresh();
//			}
//			
//		});
//		btnNoisy.addActionListener(new ActionListener() {
//			public void actionPerformed(ActionEvent e) {
//				
//			}
//		});

		GroupLayout gl_leftPanel = new GroupLayout(leftPanel);
		gl_leftPanel.setHorizontalGroup(
			gl_leftPanel.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_leftPanel.createSequentialGroup()
					.addGap(287)
					.addComponent(leftLbl)
					.addContainerGap(286, Short.MAX_VALUE))
				.addGroup(Alignment.TRAILING, gl_leftPanel.createSequentialGroup()
					.addGap(114)
					.addGroup(gl_leftPanel.createParallelGroup(Alignment.TRAILING)
						.addGroup(Alignment.LEADING, gl_leftPanel.createSequentialGroup()
							.addGap(23)
							.addComponent(btnNewButton, GroupLayout.PREFERRED_SIZE, 134, GroupLayout.PREFERRED_SIZE)
							.addPreferredGap(ComponentPlacement.RELATED, 92, Short.MAX_VALUE)
							.addComponent(btnNoisy, GroupLayout.PREFERRED_SIZE, 134, GroupLayout.PREFERRED_SIZE)
							.addGap(24))
						.addGroup(Alignment.LEADING, gl_leftPanel.createSequentialGroup()
							.addComponent(imgCountLeft, GroupLayout.PREFERRED_SIZE, 164, GroupLayout.PREFERRED_SIZE)
							.addPreferredGap(ComponentPlacement.RELATED, 86, Short.MAX_VALUE)
							.addComponent(correctCountLeft, GroupLayout.PREFERRED_SIZE, 157, GroupLayout.PREFERRED_SIZE))
						.addComponent(imageLeft, Alignment.LEADING, GroupLayout.DEFAULT_SIZE, 407, Short.MAX_VALUE))
					.addGap(115))
		);
		gl_leftPanel.setVerticalGroup(
			gl_leftPanel.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_leftPanel.createSequentialGroup()
					.addGap(38)
					.addComponent(leftLbl)
					.addGap(64)
					.addGroup(gl_leftPanel.createParallelGroup(Alignment.BASELINE)
						.addComponent(imgCountLeft)
						.addComponent(correctCountLeft))
					.addGap(12)
					.addComponent(imageLeft, GroupLayout.PREFERRED_SIZE, 425, GroupLayout.PREFERRED_SIZE)
					.addGap(18)
					.addGroup(gl_leftPanel.createParallelGroup(Alignment.BASELINE)
						.addComponent(btnNewButton, GroupLayout.PREFERRED_SIZE, 53, GroupLayout.PREFERRED_SIZE)
						.addComponent(btnNoisy, GroupLayout.PREFERRED_SIZE, 53, GroupLayout.PREFERRED_SIZE))
					.addContainerGap(51, Short.MAX_VALUE))
		);
		leftPanel.setLayout(gl_leftPanel);

		rightPanel = new JPanel();
		rightPanel.setBorder(new LineBorder(new Color(0, 0, 0)));
		split_pane.setRightComponent(rightPanel);

		rightLbl = new JLabel("AI");
		rightLbl.setHorizontalAlignment(JLabel.CENTER);
		rightLbl.setFont(new Font("Lucida Grande", Font.BOLD, 28));

		imageRight = new JLabel("");
		imageRight.setHorizontalAlignment(JLabel.CENTER);
		imageRight.setPreferredSize(new Dimension(400, 400));

		imgCountRight = new JLabel("Image Count: 0");
		imgCountRight.setFont(new Font("Lucida Grande", Font.PLAIN, 17));

		correctCountRight = new JLabel("Correct Count: 0");
		correctCountRight.setFont(new Font("Lucida Grande", Font.PLAIN, 17));
		GroupLayout gl_rightPanel = new GroupLayout(rightPanel);
		gl_rightPanel.setHorizontalGroup(gl_rightPanel.createParallelGroup(Alignment.LEADING).addGroup(gl_rightPanel
				.createSequentialGroup()
				.addGroup(gl_rightPanel.createParallelGroup(Alignment.LEADING)
						.addGroup(gl_rightPanel.createSequentialGroup().addGap(283).addComponent(rightLbl))
						.addGroup(gl_rightPanel.createSequentialGroup().addGap(119).addGroup(gl_rightPanel
								.createParallelGroup(Alignment.LEADING, false)
								.addComponent(imageRight, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE,
										GroupLayout.PREFERRED_SIZE)
								.addGroup(gl_rightPanel.createSequentialGroup()
										.addComponent(imgCountRight, GroupLayout.PREFERRED_SIZE, 160,
												GroupLayout.PREFERRED_SIZE)
										.addPreferredGap(ComponentPlacement.RELATED, GroupLayout.DEFAULT_SIZE,
												Short.MAX_VALUE)
										.addComponent(correctCountRight, GroupLayout.PREFERRED_SIZE, 165,
												GroupLayout.PREFERRED_SIZE)))))
				.addContainerGap(128, Short.MAX_VALUE)));
		gl_rightPanel.setVerticalGroup(gl_rightPanel.createParallelGroup(Alignment.LEADING).addGroup(gl_rightPanel
				.createSequentialGroup().addGap(42).addComponent(rightLbl).addGap(69)
				.addGroup(gl_rightPanel.createParallelGroup(Alignment.BASELINE)
						.addComponent(imgCountRight, GroupLayout.PREFERRED_SIZE, 21, GroupLayout.PREFERRED_SIZE)
						.addComponent(correctCountRight, GroupLayout.PREFERRED_SIZE, 21, GroupLayout.PREFERRED_SIZE))
				.addPreferredGap(ComponentPlacement.RELATED)
				.addComponent(imageRight, GroupLayout.PREFERRED_SIZE, 425, GroupLayout.PREFERRED_SIZE)
				.addContainerGap(119, Short.MAX_VALUE)));
		rightPanel.setLayout(gl_rightPanel);
		getContentPane().setLayout(groupLayout);

	}

	public void refresh() {
		BufferedImage img = null;

		if (isFileSet) {
			try {
				img = ImageIO.read(new File("/Users/li-tigre/Desktop/data/Test/" + myImages.get(imgCount)));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

			Image dimg = img.getScaledInstance(400, 400, Image.SCALE_SMOOTH);

			if (imgCount >= l - 1) {
				imgCount = 0;

			}

			// person scores
			imgCountLeft.setText("Image Count: " + totalCount);
			correctCountLeft.setText("Correct Count: " + correctCount);

			imageLeft.setIcon(new ImageIcon(dimg));

			// AI stuff
			try {
				img = ImageIO.read(new File("/Users/li-tigre/Desktop/data/Test/" + myImages.get(imgCountAI)));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

			Image dimg1 = img.getScaledInstance(400, 400, Image.SCALE_SMOOTH);

			if (imgCountAI >= l - 1) {
				imgCountAI = 0;
			}

			// person scores
			imgCountRight.setText("Image Count: " + totalCountAI);
			correctCountRight.setText("Correct Count: " + correctCountAI);
			imageRight.setIcon(new ImageIcon(dimg1));
		}
	}

	public void checkImgHuman(int arrayIndex, String userInput) {
		String answer = myLabels.get(arrayIndex);
//		System.out.println(answer);
//		System.out.println(userInput);
		if (userInput.equals(answer)) {
			correctCount++;
//			System.out.println("yup");
		}
		totalCount++;
	}

	public void checkImgAI(int arrayIndex) {
		String answer = myLabels.get(arrayIndex);
		// TODO: change to a bot answer from botarray
		if (botLabels.get(arrayIndex).equals(answer)) {
			correctCountAI++;
			// System.out.println("yup");
		}
		totalCountAI++;
	}
}
