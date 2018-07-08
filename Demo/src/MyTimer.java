import java.util.List;
import java.util.Random;

import javax.swing.JFrame;
import javax.swing.JButton;
import java.awt.BorderLayout;
import javax.swing.BoxLayout;
import javax.swing.GroupLayout;
import javax.swing.GroupLayout.Alignment;
import javax.swing.JSplitPane;
import javax.swing.LayoutStyle.ComponentPlacement;

import javax.swing.JPanel;
import javax.swing.JLabel;
import java.awt.Font;
import javax.swing.SwingConstants;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class MyTimer extends JFrame {

	JSplitPane splitPane;
	JButton startBtn;
	JLabel timerLbl;

	DemoWindow d;
	MyThread t;
	LeaderBoard l;

	public MyTimer() {

		setTitle("Timer");

		initComponents();
	}

	public MyTimer(MyThread t2, DemoWindow dm, LeaderBoard leaderboard) {
		d = dm;
		t = t2;
		l = leaderboard;
		setTitle("Timer");

		initComponents();

	}

	private void initComponents() {
		// this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		// this.setVisible(true);
		this.setAlwaysOnTop(true);
		this.setLocation(540, 175);
		this.setSize(200, 130);
		this.setResizable(false);
		// this.setFocusable(false);

		splitPane = new JSplitPane();
		splitPane.setOrientation(JSplitPane.VERTICAL_SPLIT);

		//
		//
		splitPane.setDividerSize(0);
		splitPane.setDividerLocation(75);

		GroupLayout groupLayout = new GroupLayout(getContentPane());
		groupLayout.setHorizontalGroup(groupLayout.createParallelGroup(Alignment.LEADING)
				.addGroup(groupLayout.createSequentialGroup()
						.addComponent(splitPane, GroupLayout.PREFERRED_SIZE, 201, GroupLayout.PREFERRED_SIZE)
						.addContainerGap(43, Short.MAX_VALUE)));
		groupLayout.setVerticalGroup(groupLayout.createParallelGroup(Alignment.LEADING).addComponent(splitPane,
				GroupLayout.DEFAULT_SIZE, 108, Short.MAX_VALUE));

		startBtn = new JButton("Start Timer");
		startBtn.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				startBtn.setEnabled(false);

				t.start();
				d.isPlaying = true;
				t.isPlaying = true;

				Thread thread = new Thread(new Runnable() {
					@SuppressWarnings("deprecation")
					@Override
					public void run() {
						try {
							for (int i = 1500; i > 0; i--) {
								String number = Integer.toString(i);
								while (number.length() != 4) {
									number = "0" + number;
								}

								String first = number.substring(0, number.length() / 2);
								String second = number.substring(number.length() / 2);

								timerLbl.setText(first + ":" + second);

								// String number = Integer.toString(i);
								// String n = "";
								//
								// while (n.length() != 4) {
								// for (int j = 0; i < number.length(); i++) {
								// n = number.charAt(number.length()-1-j) + n;
								// }
								// n = "0" + n;
								// }
								//
								// // if (number.length() < 4) {
								// // timerLbl.setText("0" + number.charAt(0) + ":" +
								// number.charAt(1)
								// // + number.charAt(2));
								// // }
								// // else {
								// timerLbl.setText(number.charAt(0) + number.charAt(1) + ":" +
								// number.charAt(2)
								// + number.charAt(3));
								// // }
								Thread.sleep(10);
							}
							timerLbl.setText("00:00");
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
						d.isPlaying = false;
						t.isPlaying = false;

						// update bot
						int totalAI = d.totalCountAI;
						float accuracyAI = ((float) d.correctCountAI) / ((float) totalAI);

						// for (int i = 0; i < MRAIApplication.names.size(); i++) {
						// if (MRAIApplication.names.get(i) == "AI") {
						if (MRAIApplication.totalImages.get(0) < totalAI) {
							MRAIApplication.totalImages.set(0, totalAI);
							MRAIApplication.accuracies.set(0, accuracyAI * 100);
							// }

							// break;
						}
						// }

						// update humans
						List<Integer> scores = MRAIApplication.totalImages;

						int totalHuman = d.totalCount;
						float accuracyHuman = ((float) d.correctCount) / ((float) totalHuman);

						// Integer max = 0;
						boolean added = false;
						for (int i = 0; i < scores.size(); i++) {
							if (scores.get(i) < totalHuman) {
								MRAIApplication.names.add(i, MRAIApplication.tempName);
								MRAIApplication.totalImages.add(i, totalHuman);
								MRAIApplication.accuracies.add(i, accuracyHuman * 100);
								added = true;
								break;
							}

						}
						if (!added) {
							MRAIApplication.names.add(MRAIApplication.tempName);
							MRAIApplication.totalImages.add(totalHuman);
							if (totalHuman == 0) {
								MRAIApplication.accuracies.add((float) 0);
							}
							else {
								MRAIApplication.accuracies.add(accuracyHuman * 100);
							}
						}
						MRAIApplication.tempName = "";

						// for (Integer score: scores) {
						// if (!(score > totalHuman)) {
						// scores.
						// }
						//
						// }

						// TODO: refresh leaderboard

						try {
							Thread.sleep(1000);
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}

						l.setVisible(true);
						l.refresh();

					}
				});
				thread.start();

				d.toFront();

			}
		});
		splitPane.setRightComponent(startBtn);

		timerLbl = new JLabel("00:00");
		timerLbl.setHorizontalAlignment(SwingConstants.CENTER);
		timerLbl.setFont(new Font("Lucida Grande", Font.BOLD, 38));
		splitPane.setLeftComponent(timerLbl);
		getContentPane().setLayout(groupLayout);

		setEnabled(false);

	}

	public void close() {
		this.setVisible(false);
		this.dispose();
	}
}
