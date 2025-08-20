import React, { useState } from "react"

type Message = {
  id: number
  text: string
}

export default function Messenger() {
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, text: "Hello!" },
    { id: 2, text: "How are you?" },
    { id: 3, text: "This will be deleted if you click ❌" },
  ])

  const deleteMessage = (id: number) => {
    // remove message from state (UI)
    setMessages((prev) => prev.filter((msg) => msg.id !== id))

    // Optionally, send request to backend to delete from DB
    // fetch(`/api/messages/${id}`, { method: "DELETE", headers: { Authorization: `Bearer ${token}` } })
  }

  return (
    <div className="max-w-md mx-auto p-4 bg-gray-100 rounded-2xl shadow">
      <h2 className="text-xl font-bold mb-3">Chat</h2>
      <div className="space-y-2">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className="flex justify-between items-center bg-white p-3 rounded-xl shadow-sm"
          >
            <span>{msg.text}</span>
            <button
              onClick={() => deleteMessage(msg.id)}
              className="text-red-500 hover:text-red-700 font-bold"
            >
              ❌
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
