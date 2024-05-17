-- attach the modem
local modem = peripheral.find("modem")

-- open modem on channel
local channel = 1
modem.open(channel)

-- function to wrap the speakers
local function findSpeakers()
    -- instantiate with some stuf
    local speakers = {}
    local sides = {"left", "right", "top", "bottom", "front", "back"}

    -- check each side of the computer for speaker
    for _, side in ipairs(sides) do
        if peripheral.isPresent(side) and peripheral.getType(side) == "speaker" then
            table.insert(speakers, peripheral.wrap(side))
        end
    end
    return speakers
end

-- function for playing a sound
local function playSoundOnSpeakers(speakers, sound, volume, pitch)
    for _, speaker in ipairs(speakers) do
        speaker.playSound(sound, volume, pitch)
    end
end

-- 'main' function
-- listens to the channel and plays received sounds
while true do
    local event, side, receivedChannel, replyChannel, message, distance = os.pullEvent("modem_message")
    if receivedChannel == channel then
        local speakers = findSpeakers()
        if #speakers > 0 then
            local sound = message.sound
            local volume = message.volume
            local pitch = message.pitch
            playSoundOnSpeakers(speakers, sound, volume, pitch)
        else
            print("No speakers are attached. womp womp")
        end
    end
end