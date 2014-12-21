package com.bibimbot.ircbotscheduler.scheduler;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;

public class SchedulerClient {
	static Socket socket;
	static PrintWriter out;
	
	
	public SchedulerClient(String serverAddress, String port) throws NumberFormatException, UnknownHostException, IOException {
		socket = new Socket(serverAddress, Integer.parseInt(port));
	}
	
	public static void main(String[] args) throws NumberFormatException, UnknownHostException, IOException {
		SchedulerClient client = new SchedulerClient(args[0], args[1]);
		out = new PrintWriter(socket.getOutputStream(), true);
		Scanner sc = new Scanner(System.in);
		String input;
		printCommands();
		while (true) {
			input = sc.nextLine();
			if (input.equals("?exit")) {
				out.println(input);
				break;
			}
			out.println(input);
		}
		out.close();
		sc.close();
		socket.close();
	}
	
	private static void printCommands() {
		System.out.println("Welcome to the Scheduler Client!\n " +
				"tweet with one bot -- ?tweet [botname] [message]\n" +
                "delete tweets -- ?deleteTweets [botname] [numtweets]" +
                "add bots to group -- ?addToGroup [bot1,bot2,etc] [botgroup]" +
                "display groups and bots -- ?displayGroups" +
				"tweet with group of bots -- ?tweet group:[botgroup] [message]\n" +
                "repost attack -- ?repostAttack [link]" +
				"schedule -- schedule [time(Seconds)] [command]\n");
	}
}
