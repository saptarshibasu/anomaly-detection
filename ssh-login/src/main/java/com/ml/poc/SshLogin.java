package com.ml.poc;

import java.io.ByteArrayOutputStream;
import java.util.Random;

import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

public class SshLogin {

    public static void main(String args[]) throws Exception {
        String username = args[1];
        String password = args[2];
        String host = args[0];
        int port = 22;
        String command = "ls /";
        Random random = new Random();
        while(true) {
            listFolderStructure(username, password, host, port, command, random);
        }
    }

    public static String listFolderStructure(String username, String password, String host, int port, String command, Random random) throws Exception {
        Session session = null;
        ChannelExec channel = null;
        String response = null;
        try {
            session = new JSch().getSession(username, host, port);
            session.setPassword(password);
            session.setConfig("StrictHostKeyChecking", "no");
            session.connect();
            channel = (ChannelExec) session.openChannel("exec");
            channel.setCommand(command);
            ByteArrayOutputStream responseStream = new ByteArrayOutputStream();
            ByteArrayOutputStream errorResponseStream = new ByteArrayOutputStream();
            channel.setOutputStream(responseStream);
            channel.setErrStream(errorResponseStream);
            channel.connect();
            while (channel.isConnected()) {
                Thread.sleep(random.nextInt(1000));
            }
            String errorResponse = new String(errorResponseStream.toByteArray());
            response = new String(responseStream.toByteArray());
            System.out.println(response);
            if(!errorResponse.isEmpty()) {
                throw new Exception(errorResponse);
            }
        } finally {
            if (session != null) {
                session.disconnect();
            }
            if (channel != null) {
                channel.disconnect();
            }
        }
        return response;
    }
}
