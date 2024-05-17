-- attach the modem
local modem = peripheral.find("modem")

-- function to send a sound to a channel
local function sendSoundCommand(channel, sound, volume, pitch)
    local message = {
        sound = sound,
        volume = volume,
        pitch = pitch
    }
    modem.transmit(channel, channel, message)
end

-- set our channel
local channel = 1

-- construct the sound
sound = "minecraft:block.note_block.bell"
volume = 1.0
pitch = 1.0

-- send the sound
sendSoundCommand(channel, sound, volume, pitch)