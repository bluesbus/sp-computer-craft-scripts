local modem = peripheral.find("modem") or error("No modem attached", 0)
modem.open(15) -- Open the channel for listening

local speaker = peripheral.find("speaker") or error("No speaker attached", 0)

print("Listening for audio chunks...")

while true do
    local event, side, channel, replyChannel, message, distance = os.pullEvent("modem_message")
    if channel == 15 then
        local buffer = message
        while not speaker.playAudio(buffer) do
            os.pullEvent("speaker_audio_empty")
        end
    end
end