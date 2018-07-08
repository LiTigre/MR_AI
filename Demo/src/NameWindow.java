import javax.swing.JFrame;
import javax.swing.GroupLayout;
import javax.swing.GroupLayout.Alignment;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JButton;
import javax.swing.LayoutStyle.ComponentPlacement;
import java.awt.Font;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class NameWindow extends JFrame {
	
	
	private JTextField textField;
	JLabel lblPleaseInputYour;
	JButton btnStartChallenge;
	
	
	public NameWindow() {
		initComponents();
	}

	private void initComponents() {
		this.setAlwaysOnTop(true);
		this.setLocation(520, 200);
		this.setSize(250, 175);
		this.setResizable(false);
		
		lblPleaseInputYour = new JLabel("Please input your name");
		lblPleaseInputYour.setFont(new Font("Lucida Grande", Font.PLAIN, 17));
		
		textField = new JTextField();
		textField.setFont(new Font("Lucida Grande", Font.PLAIN, 16));
		textField.setColumns(10);
		
		btnStartChallenge = new JButton("Enter name");
		btnStartChallenge.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				MRAIApplication.tempName = textField.getText();
				MRAIApplication.dm.close();
				MRAIApplication.lb.close();
				MRAIApplication.t.close();
				MRAIApplication.reset();
				close();
				
				
				
			}
		});
		GroupLayout groupLayout = new GroupLayout(getContentPane());
		groupLayout.setHorizontalGroup(
			groupLayout.createParallelGroup(Alignment.LEADING)
				.addGroup(groupLayout.createSequentialGroup()
					.addGroup(groupLayout.createParallelGroup(Alignment.LEADING)
						.addGroup(groupLayout.createSequentialGroup()
							.addGap(29)
							.addGroup(groupLayout.createParallelGroup(Alignment.LEADING, false)
								.addComponent(textField)
								.addComponent(lblPleaseInputYour, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
						.addGroup(groupLayout.createSequentialGroup()
							.addGap(62)
							.addComponent(btnStartChallenge)))
					.addContainerGap(30, Short.MAX_VALUE))
		);
		groupLayout.setVerticalGroup(
			groupLayout.createParallelGroup(Alignment.LEADING)
				.addGroup(groupLayout.createSequentialGroup()
					.addGap(22)
					.addComponent(lblPleaseInputYour)
					.addPreferredGap(ComponentPlacement.UNRELATED)
					.addComponent(textField, GroupLayout.PREFERRED_SIZE, 36, GroupLayout.PREFERRED_SIZE)
					.addPreferredGap(ComponentPlacement.RELATED, 27, Short.MAX_VALUE)
					.addComponent(btnStartChallenge)
					.addContainerGap())
		);
		getContentPane().setLayout(groupLayout);
		
		
		
		
		
	}
	public void close() {
		this.setVisible(false);
		this.dispose();
	}
}
