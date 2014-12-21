package com.bibimbot.ircbotscheduler.scheduler;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Properties;
import java.util.Set;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class SchedulerServer {
	static ServerSocket listener;
	static Socket socket;
	static ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
	static BufferedReader reader;
	static IRCClient client;
	
	static String propFileName = "botgroups.prop";
	static Properties prop = new Properties();
	static FileInputStream inputStream;
	static FileOutputStream outputStream; 
	
	
	public SchedulerServer(String port) throws UnknownHostException, IOException {
		// Startup IRC Client
		client = new IRCClient("ix.undernet.org", "scheduler", "scheduler", "#flock");
		client.start();
		try {
			listener = new ServerSocket(Integer.parseInt(port));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static void schedule(String time, final String command) {
		scheduler.schedule(new Runnable(){
			@Override
			public void run() {
				// TODO Auto-generated method stub
				try {
					tweet(command);
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}, Integer.parseInt(time), TimeUnit.SECONDS);
	}
	public static void scheduleRepeated() {
		
	}
	
	public static void tweet(String command) throws IOException {
		String[] splitCommand = command.split(" ");
		String botname = splitCommand[1];
		String msg = command.substring(command.indexOf(botname) + botname.length() + 1);
		System.out.println(msg);
		List<String> bots;
		if (botname.contains("group:")) {
			String group = botname.substring(botname.indexOf(":")+1);
			bots = getBotsInGroup(group);
			for (String bot : bots) {
				client.send("?tweet " + bot + " " + msg);
			}
		} else {
			client.send("?tweet " + botname + " " + msg);
		}
	}
	
	public static void main(String[] args) throws UnknownHostException, IOException {
		SchedulerServer server = new SchedulerServer(args[0]);

		String command;
		try {
			socket = listener.accept();
			reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			while ((command = reader.readLine()) != null) {
				if (command.contains("schedule")) {
					String[] splitCommand = command.split(" ");
					String time = splitCommand[1];
					String prefix = splitCommand[0] + " " + time;
					String commandToRun = command.substring(command.indexOf(prefix) + prefix.length() + 1);
					schedule(time, commandToRun);
				} else if (command.contains("?tweet")) {
					tweet(command);
				} else if (command.contains("?displayGroups")) {
                    System.out.println(displayGroups());
                } else if (command.contains("?addToGroup")) {
                    String[] splitCommand = command.split(" ");
                    String botNames = splitCommand[1];
                    String botGroup = splitCommand[2];
                    addToGroup(botNames, botGroup);
                    System.out.println(displayGroups());
                } else if (command.contains("deleteTweets")) {
                    String[] splitCommand = command.split(" ");
                    String botName = splitCommand[1];
                    int numTweets = Integer.parseInt(splitCommand[2]);
                    deleteTweets(botName, numTweets);
                } else if (command.contains("repostAttack")) {
                    String[] splitCommand = command.split(" ");
                    String link = splitCommand[1];
                    repostAttack(link);
                }
				// server.client.send(command);
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		try {
			socket.close();
			listener.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	private static void addToGroup(String botNames, String botGroup) throws IOException {
		// Load properties file
		inputStream = new FileInputStream(propFileName);
		prop.load(inputStream);
		if (inputStream == null) {
			throw new FileNotFoundException("property file '" + propFileName + "' not found in the classpath");
		}
		inputStream.close();
		
		String botsString = prop.getProperty(botGroup);
		if (botsString == null) {			
            // Create group
			prop.setProperty(botGroup, botNames);
			outputStream = new FileOutputStream(propFileName);
			prop.store(outputStream, "");
			outputStream.close();
		}	
        // Check for each bot if in group already
        if (botsString != null) {
            List<String> existingBotsList = Arrays.asList(botsString.split(",")); 
            List<String> addBotsList = Arrays.asList(botNames.split(","));
            StringBuffer sBuf = new StringBuffer();
            for (String bot : addBotsList) {
                if (!existingBotsList.contains(bot)) {
                    sBuf.append("," + bot);
                }
                prop.setProperty(botGroup, botsString.concat(sBuf.toString()));
                outputStream = new FileOutputStream(propFileName);
                prop.store(outputStream, "");
                outputStream.close();
            }
        }
	}
	
	private void removeFromGroup(String botName, String botGroup) {
		
	}
	
	private static String displayGroups() throws IOException {
		StringBuffer strBuf = new StringBuffer();
        strBuf.append("-----Groups-----");
		inputStream = new FileInputStream(propFileName);
		prop.load(inputStream);
		if (inputStream == null) {
			throw new FileNotFoundException("property file '" + propFileName + "' not found in the classpath");
		}
		inputStream.close();
		Set<String> props = prop.stringPropertyNames();
		Iterator<String> i = props.iterator();
		String group;
		String bots;
		while (i.hasNext()) {
			group = i.next().toString();
			bots = prop.getProperty(group);
			strBuf.append(group + ":\n" + bots + "\n\n");
		}
		return strBuf.toString();
	}
	
	private static List<String> getBotsInGroup(String group) throws IOException {
		inputStream = new FileInputStream(propFileName);
		prop.load(inputStream);
		if (inputStream == null) {
			throw new FileNotFoundException("property file '" + propFileName + "' not found in the classpath");
		}
		inputStream.close();
		
		String bots = prop.getProperty(group);
		return Arrays.asList(bots.split(","));
	}

    private static void deleteTweets(String botName, int numTweets) throws IOException {
        client.send("?deletetweets " + botName + " " + numTweets);
    }

    private static void repostAttack(String link) throws IOException {
        client.send("?repostattack " + link);
    }
}
