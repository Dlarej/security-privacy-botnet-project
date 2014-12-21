package com.bibimbot.ircbotscheduler.scheduler;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class IRCClient {
	Socket socket;
	String server;
	String nick;
	String login;
	String channel;
	BufferedWriter writer;
	BufferedReader reader;
	
	public IRCClient(String server, String nick, String login, String channel) throws UnknownHostException, IOException {
		socket = new Socket(server, 6667);
		this.server = server;
		this.nick = nick;
		this.login = login;
		this.channel = channel;
	}
	
	public void start() throws IOException {
		writer = new BufferedWriter(
				new OutputStreamWriter(socket.getOutputStream()));
		reader = new BufferedReader(
	            new InputStreamReader(socket.getInputStream( )));
		// Log on to the server.
        writer.write("NICK " + nick + "\r\n");
        writer.flush( );
        writer.write("USER " + login + " 8 * : Java IRC Hacks Bot\r\n");
        writer.flush( );
        
        String line = null;
        while ((line = reader.readLine( )) != null) {
            if (line.toLowerCase( ).startsWith("ping ")) {
                // We must respond to PINGs to avoid being disconnected.
                writer.write("PONG " + line.substring(5) + "\r\n");
                writer.flush( );
            } else if (line.indexOf("004") >= 0) {
            	System.out.println("Logged in");
            	break;
            } else {
                // Print the raw line received by the bot.
                System.out.println(line);
            }
        }
        // Join the channel.
        writer.write("JOIN " + channel + "\r\n");
        writer.flush( );
        
        new Thread(new Runnable() {
			@Override
			public void run() {
				// TODO Auto-generated method stub
				try {
					rcv();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
        }).start();
	}
	
	private void rcv() throws IOException {
		// Read lines from the server until it tells us we have connected.
        String line = null;
        // Keep reading lines from the server.
        while ((line = reader.readLine( )) != null) {
            if (line.toLowerCase( ).startsWith("ping ")) {
                // We must respond to PINGs to avoid being disconnected.
                writer.write("PONG " + line.substring(5) + "\r\n");
                writer.flush( );
            }
            else {
                // Print the raw line received by the bot.
                System.out.println(line);
            }
        }
	}
	public void send(String message) throws IOException {
        writer.write("PRIVMSG " + channel + " :" + message + "\r\n");
        writer.flush( );
	}
}
