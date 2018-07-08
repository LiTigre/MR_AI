import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.GroupLayout;
import javax.swing.GroupLayout.Alignment;
import javax.swing.JSplitPane;
import javax.swing.JTextPane;
import javax.swing.JButton;
import java.awt.Font;
import java.awt.Color;
import javax.swing.JLabel;
import javax.swing.LayoutStyle.ComponentPlacement;

import java.awt.event.ActionListener;
import java.util.List;
import java.awt.event.ActionEvent;

public class LeaderBoard extends JFrame {

	JSplitPane splitPane;
	JButton startBtn;
	JPanel textPanel;
	private JLabel lblNewLabel;
	private JSplitPane text_split;
	private JTextPane names;
	private JTextPane scores;
	private JLabel lblNames;
	private JLabel lblOfImages;
	private JLabel lblAccuracy;

	public LeaderBoard() {

		setTitle("LeaderBoard");

		initComponents();
	}

	private void initComponents() {
		this.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
		this.setAlwaysOnTop(true);
		this.setLocation(450, 100);
		this.setSize(400, 600);
		this.setResizable(false);

		splitPane = new JSplitPane();
		splitPane.setOrientation(JSplitPane.VERTICAL_SPLIT);
		splitPane.setDividerSize(0);
		splitPane.setDividerLocation(500);

		GroupLayout groupLayout = new GroupLayout(getContentPane());
		groupLayout.setHorizontalGroup(
				groupLayout.createParallelGroup(Alignment.LEADING).addGroup(groupLayout.createSequentialGroup()
						.addComponent(splitPane, GroupLayout.PREFERRED_SIZE, 401, Short.MAX_VALUE).addContainerGap()));
		groupLayout.setVerticalGroup(groupLayout.createParallelGroup(Alignment.LEADING)
				.addGroup(groupLayout.createSequentialGroup()
						.addComponent(splitPane, GroupLayout.PREFERRED_SIZE, 578, GroupLayout.PREFERRED_SIZE)
						.addContainerGap(382, Short.MAX_VALUE)));

		textPanel = new JPanel();
		textPanel.setBackground(Color.WHITE);
		splitPane.setLeftComponent(textPanel);

		lblNewLabel = new JLabel("Top Challengers");
		lblNewLabel.setFont(new Font("Lucida Grande", Font.BOLD, 23));

		text_split = new JSplitPane();
		text_split.setBorder(null);

		text_split.setOrientation(JSplitPane.HORIZONTAL_SPLIT);
		text_split.setBackground(Color.WHITE);
		// text_split.setLeftComponent(names);
		// text_split.setRightComponent(scores);
		text_split.setDividerLocation(200);
		text_split.setDividerSize(0);
		
		lblNames = new JLabel("Names");
		
		lblOfImages = new JLabel("# of images");
		
		lblAccuracy = new JLabel("accuracy");

		GroupLayout gl_textPanel = new GroupLayout(textPanel);
		gl_textPanel.setHorizontalGroup(
			gl_textPanel.createParallelGroup(Alignment.LEADING)
				.addComponent(text_split, GroupLayout.DEFAULT_SIZE, 397, Short.MAX_VALUE)
				.addGroup(gl_textPanel.createSequentialGroup()
					.addGroup(gl_textPanel.createParallelGroup(Alignment.LEADING, false)
						.addGroup(gl_textPanel.createSequentialGroup()
							.addGap(98)
							.addComponent(lblNewLabel)
							.addGap(12)
							.addPreferredGap(ComponentPlacement.RELATED))
						.addGroup(gl_textPanel.createSequentialGroup()
							.addGap(58)
							.addComponent(lblNames)
							.addPreferredGap(ComponentPlacement.RELATED, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
							.addComponent(lblOfImages)
							.addGap(37)))
					.addComponent(lblAccuracy)
					.addContainerGap(40, Short.MAX_VALUE))
		);
		gl_textPanel.setVerticalGroup(
			gl_textPanel.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_textPanel.createSequentialGroup()
					.addGap(14)
					.addComponent(lblNewLabel)
					.addGap(17)
					.addGroup(gl_textPanel.createParallelGroup(Alignment.BASELINE)
						.addComponent(lblNames)
						.addComponent(lblAccuracy)
						.addComponent(lblOfImages))
					.addPreferredGap(ComponentPlacement.UNRELATED)
					.addComponent(text_split, GroupLayout.PREFERRED_SIZE, 412, GroupLayout.PREFERRED_SIZE)
					.addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
		);

		names = new JTextPane();
		names.setEditable(false);
		text_split.setLeftComponent(names);

		scores = new JTextPane();
		scores.setEditable(false);
		text_split.setRightComponent(scores);
		textPanel.setLayout(gl_textPanel);

		startBtn = new JButton("Start Again");
		startBtn.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				MRAIApplication.newGame();

			}
		});
		startBtn.setFont(new Font("Lucida Grande", Font.PLAIN, 28));
		splitPane.setRightComponent(startBtn);
		getContentPane().setLayout(groupLayout);
		names.setText("    ");
		scores.setText("  ");

	}

	public void refresh() {
		List<String> n = MRAIApplication.names;
		List<Float> a = MRAIApplication.accuracies;
		List<Integer> t = MRAIApplication.totalImages;

		int max = 0;

		for (int i = 0; i < 10 && i < n.size(); i++) {
			names.setText(names.getText() + "    " + Integer.toString(i + 1) + ".\t" + n.get(i) + "\n\n" + "    ");
			scores.setText(scores.getText() + "  " + Integer.toString(t.get(i)) + "\t        "
					+ String.format("%.2f", a.get(i)) + "%" + "\n\n" + "  ");

		}

	}

	int[] toIntArray(List<Integer> list) {
		int[] ret = new int[list.size()];
		int i = 0;
		for (Integer e : list)
			ret[i++] = e.intValue();
		return ret;
	}

	public void close() {
		this.setVisible(false);
		this.dispose();
	}
}
