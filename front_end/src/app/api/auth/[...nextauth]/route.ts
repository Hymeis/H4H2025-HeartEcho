// api/auth/[...nextauth]/route.ts
import NextAuth, { AuthOptions } from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';

export const authOptions: AuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
    }),
  ],
  callbacks: {
    async jwt({ token, account, profile }) {
      if (account && profile && profile.email) {
        try {
          const response = await fetch('http://localhost:5000/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: profile.email }),
          });

          if (!response.ok) {
            console.error('Failed to register user in Flask', await response.text());
          } else {
            const data = await response.json();
            token.uid = data.uid;
          }
        } catch (err) {
          console.error('Error calling Flask /register:', err);
        }
      }

      return token;
    },

    // Called when NextAuth returns the session object to the frontend
    async session({ session, token }) {
      if (token.uid) {
        if (session && session.user) {
          session.user.uid = token.uid as string;
        }
        
      }
      return session;
    },

    async signIn({ profile }) {
      if (profile?.email?.endsWith('@scu.edu')) {
        return true;
      }
      return false;
    },
  },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
