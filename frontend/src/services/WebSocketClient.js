class WebSocketClient {

  constructor() {

    this.socket = null;
  }


  // =========================================
  // CONNECT
  // =========================================

  connect() {

    this.socket = new WebSocket(

      "ws://127.0.0.1:8000/ws"
    );


    // =====================================
    // OPEN
    // =====================================

    this.socket.onopen = () => {

      console.log(

        "✅ WebSocket Connected"
      );
    };


    // =====================================
    // MESSAGE
    // =====================================

    this.socket.onmessage = (
      event
    ) => {

      console.log(

        "📩 Message:",

        event.data
      );
    };


    // =====================================
    // CLOSE
    // =====================================

    this.socket.onclose = () => {

      console.log(

        "⚠️ WebSocket Disconnected"
      );
    };


    // =====================================
    // ERROR
    // =====================================

    this.socket.onerror = (
      error
    ) => {

      console.log(

        "❌ WebSocket Error",

        error
      );
    };
  }


  // =========================================
  // SEND MESSAGE
  // =========================================

  sendMessage(message) {

    if (

      this.socket &&

      this.socket.readyState ===
      WebSocket.OPEN

    ) {

      this.socket.send(message);
    }
  }


  // =========================================
  // DISCONNECT
  // =========================================

  disconnect() {

    if (this.socket) {

      this.socket.close();
    }
  }
}


// =============================================
// CREATE INSTANCE
// =============================================

const websocketClient =
  new WebSocketClient();


// =============================================
// EXPORT
// =============================================

export default websocketClient;