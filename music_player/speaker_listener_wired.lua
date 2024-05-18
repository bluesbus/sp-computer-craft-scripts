local function get_all_speakers()
    local speakers = { peripheral.find("speaker") }
    if #speakers == 0 then
        error("No speakers attached", 0)
    end
    return speakers
end

local modem = peripheral.find("modem") or error("No modem attached", 0)
modem.open(15) -- Open the channel for listening

local speakers = get_all_speakers()

print("Listening for audio chunks...")

while true do
    local event, side, channel, replyChannel, message, distance = os.pullEvent("modem_message")
    if channel == 15 then
        local buffer = message
        for _, speaker in ipairs(speakers) do
            while not speaker.playAudio(buffer) do
                os.pullEvent("speaker_audio_empty")
            end
        end
    end
end
