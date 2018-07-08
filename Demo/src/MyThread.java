import java.util.Random;

public class MyThread extends Thread {
	DemoWindow dm;
	boolean isPlaying = false;

	public MyThread(DemoWindow demo_window) {
		dm = demo_window;
	}

	public void run() {
		while (isPlaying) {

			dm.checkImgAI(dm.imgCountAI); // TODO: change the second input
			dm.imgCountAI++;
			dm.refresh();
			try {
				int sleepTime = getRandomNumberInRange(1, 30);
				
				sleep(sleepTime);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
//			System.out.println("MyThread running");

		}
	}
	
	private static int getRandomNumberInRange(int min, int max) {

		if (min >= max) {
			throw new IllegalArgumentException("max must be greater than min");
		}

		Random r = new Random();
		return r.nextInt((max - min) + 1) + min;
	}
}