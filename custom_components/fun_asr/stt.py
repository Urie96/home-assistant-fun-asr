import logging
import aiohttp
from collections.abc import AsyncIterable

from homeassistant.components import stt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([FasterASRSTT(hass, config_entry)])


class FasterASRSTT(stt.SpeechToTextEntity):
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        server: str = config_entry.data["server"]
        self.server = server
        self._attr_name = f"Fun Asr({server})"
        self._attr_unique_id = f"{config_entry.entry_id[:7]}-fun-asr"

    @property
    def supported_languages(self) -> list[str]:
        return ["zh"]

    @property
    def supported_formats(self) -> list[stt.AudioFormats]:
        return [stt.AudioFormats.WAV]

    @property
    def supported_codecs(self) -> list[stt.AudioCodecs]:
        return [stt.AudioCodecs.PCM]

    @property
    def supported_bit_rates(self) -> list[stt.AudioBitRates]:
        return [stt.AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[stt.AudioSampleRates]:
        return [stt.AudioSampleRates.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[stt.AudioChannels]:
        return [stt.AudioChannels.CHANNEL_MONO]

    async def async_process_audio_stream(
        self, metadata: stt.SpeechMetadata, stream: AsyncIterable[bytes]
    ) -> stt.SpeechResult:
        _LOGGER.debug("process_audio_stream start")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.server, data=stream) as resp:
                    if resp.status == 200:
                        result = await resp.text()
                        _LOGGER.debug(f"process_audio_stream end: {result}")

                        return stt.SpeechResult(result, stt.SpeechResultState.SUCCESS)

        except Exception as err:
            _LOGGER.exception("Error processing audio stream: %s", err)
            return stt.SpeechResult(
                "识别出现异常，请检查配置是否正确", stt.SpeechResultState.SUCCESS
            )

        return stt.SpeechResult(None, stt.SpeechResultState.ERROR)
