import React, { useState } from 'react';
import styles from './styles.module.css';

export default function ChatBot() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: '👋 Hi! Ask me anything about the book!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setLoading(true);
    setInput('');

    try {
      // ✅ ENDPOINT CHANGED: /query → /ask
      const response = await fetch('https://abdulrehman120-rag-chatbot.hf.space/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          query: input  // ✅ KEY CHANGED: question → query
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Backend response:', data);  // Debug log
      
      const botMessage = { 
        role: 'assistant', 
        // ✅ Backend returns 'answer' key
        content: data.answer || 'No response received'
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        role: 'error', 
        content: `❌ Connection failed! ${error.message}` 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatHeader}>
        <div>
          <h3 className={styles.chatTitle}>🤖 AI Assistant</h3>
          <span className={styles.chatSubtitle}>Powered by RAG</span>
        </div>
        <span className={styles.statusBadge}>● Online</span>
      </div>

      <div className={styles.messagesContainer}>
        {messages.map((msg, idx) => (
          <div 
            key={idx} 
            className={`${styles.message} ${styles[msg.role]}`}
          >
            <div className={styles.messageContent}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className={styles.loading}>
            <div className={styles.typingIndicator}>
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
      </div>

      <div className={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
          placeholder="Type your question..."
          className={styles.input}
          disabled={loading}
        />
        <button 
          onClick={sendMessage} 
          className={styles.sendButton}
          disabled={loading || !input.trim()}
        >
          <span className={styles.sendIcon}>➤</span>
        </button>
      </div>
    </div>
  );
}