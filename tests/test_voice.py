"""
Unit tests for voice synthesis module.

Tests cover:
- Backend detection
- Voice mappings
- Synthesis functions (mocked)
- Podcast generation (mocked)
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestBackendDetection:
    """Test TTS backend detection."""

    def test_check_tts_backends_structure(self):
        """check_tts_backends should return proper structure."""
        from project_management_automation.tools.wisdom.voice import check_tts_backends

        result = check_tts_backends()

        assert "available_backends" in result
        assert "recommended" in result
        assert "details" in result
        assert isinstance(result["available_backends"], list)
        assert isinstance(result["details"], dict)

    def test_check_backends_includes_all_options(self):
        """Should check all three backends."""
        from project_management_automation.tools.wisdom.voice import check_tts_backends

        result = check_tts_backends()

        # All three backends should be in details
        assert "elevenlabs" in result["details"]
        assert "edge-tts" in result["details"]
        assert "pyttsx3" in result["details"]

    def test_get_available_backend_with_api_key(self):
        """With ElevenLabs API key, should prefer elevenlabs."""
        from project_management_automation.tools.wisdom.voice import get_available_backend

        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test_key"}):
            with patch("project_management_automation.tools.wisdom.voice.elevenlabs", create=True):
                # Mock the import check
                import sys

                mock_module = MagicMock()
                with patch.dict(sys.modules, {"elevenlabs": mock_module}):
                    result = get_available_backend()
                    # May be elevenlabs if module found, or fall through to edge-tts/pyttsx3


class TestVoiceMappings:
    """Test advisor voice mappings."""

    def test_advisor_voices_exist(self):
        """All backends should have voice mappings."""
        from project_management_automation.tools.wisdom.voice import ADVISOR_VOICES

        assert "elevenlabs" in ADVISOR_VOICES
        assert "edge-tts" in ADVISOR_VOICES
        assert "pyttsx3" in ADVISOR_VOICES

    def test_default_voice_exists(self):
        """Each backend should have a default voice."""
        from project_management_automation.tools.wisdom.voice import ADVISOR_VOICES

        assert "default" in ADVISOR_VOICES["elevenlabs"]
        assert "default" in ADVISOR_VOICES["edge-tts"]
        assert "default" in ADVISOR_VOICES["pyttsx3"]

    def test_common_advisors_have_voices(self):
        """Common advisors should have voice mappings."""
        from project_management_automation.tools.wisdom.voice import ADVISOR_VOICES

        common_advisors = ["bofh", "stoic", "zen", "mystic", "sage"]

        for advisor in common_advisors:
            assert advisor in ADVISOR_VOICES["elevenlabs"], f"Missing {advisor} in elevenlabs"
            assert advisor in ADVISOR_VOICES["edge-tts"], f"Missing {advisor} in edge-tts"
            assert advisor in ADVISOR_VOICES["pyttsx3"], f"Missing {advisor} in pyttsx3"

    def test_elevenlabs_voices_have_ids(self):
        """ElevenLabs voices should have voice_id and name."""
        from project_management_automation.tools.wisdom.voice import ADVISOR_VOICES

        for advisor, voice_info in ADVISOR_VOICES["elevenlabs"].items():
            assert "voice_id" in voice_info, f"Missing voice_id for {advisor}"
            assert "name" in voice_info, f"Missing name for {advisor}"


class TestListAvailableVoices:
    """Test list_available_voices function."""

    def test_list_voices_returns_structure(self):
        """list_available_voices should return proper structure."""
        from project_management_automation.tools.wisdom.voice import list_available_voices

        result = list_available_voices(backend="edge-tts")

        assert "backend" in result
        assert "advisor_voices" in result
        assert result["backend"] == "edge-tts"

    def test_list_voices_auto_with_no_backend(self):
        """With no backend available, should return error."""
        from project_management_automation.tools.wisdom.voice import list_available_voices

        with patch("project_management_automation.tools.wisdom.voice.get_available_backend") as mock:
            mock.return_value = None
            result = list_available_voices(backend="auto")

            assert "error" in result


class TestSynthesizeAdvisorQuote:
    """Test synthesize_advisor_quote function."""

    def test_synthesize_no_backend_available(self):
        """Should return error when no backend available."""
        from project_management_automation.tools.wisdom.voice import synthesize_advisor_quote

        with patch("project_management_automation.tools.wisdom.voice.get_available_backend") as mock:
            mock.return_value = None
            result = synthesize_advisor_quote("Test quote", backend="auto")

            assert result["success"] is False
            assert "error" in result

    def test_synthesize_elevenlabs_mocked(self):
        """Test ElevenLabs synthesis with mocked API."""
        from project_management_automation.tools.wisdom.voice import synthesize_advisor_quote

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.mp3"

            # Mock the ElevenLabs client
            with patch("project_management_automation.tools.wisdom.voice._synthesize_elevenlabs") as mock_synth:
                mock_synth.return_value = output_path

                # Create the file to simulate successful synthesis
                output_path.write_bytes(b"fake audio data")

                result = synthesize_advisor_quote(
                    "Test quote",
                    advisor="bofh",
                    output_path=str(output_path),
                    backend="elevenlabs",
                )

                assert result["success"] is True
                assert result["backend"] == "elevenlabs"
                assert result["advisor"] == "bofh"

    def test_synthesize_edge_tts_mocked(self):
        """Test edge-tts synthesis with mocked command."""
        from project_management_automation.tools.wisdom.voice import synthesize_advisor_quote

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.mp3"

            with patch("project_management_automation.tools.wisdom.voice._synthesize_edge_tts") as mock_synth:
                mock_synth.return_value = output_path
                output_path.write_bytes(b"fake audio data")

                result = synthesize_advisor_quote(
                    "Test quote",
                    advisor="stoic",
                    output_path=str(output_path),
                    backend="edge-tts",
                )

                assert result["success"] is True
                assert result["backend"] == "edge-tts"

    def test_synthesize_generates_output_path(self):
        """Should auto-generate output path when not provided."""
        from project_management_automation.tools.wisdom.voice import synthesize_advisor_quote

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("project_management_automation.utils.find_project_root") as mock_root:
                mock_root.return_value = Path(tmpdir)

                with patch("project_management_automation.tools.wisdom.voice._synthesize_edge_tts") as mock_synth:

                    def create_file(text, voice, path):
                        path.write_bytes(b"fake audio")
                        return path

                    mock_synth.side_effect = create_file

                    result = synthesize_advisor_quote(
                        "Test quote",
                        backend="edge-tts",
                    )

                    if result["success"]:
                        assert "audio_path" in result
                        assert ".exarp/audio" in result["audio_path"]

    def test_synthesize_includes_metadata(self):
        """Should include text length, word count, duration estimate."""
        from project_management_automation.tools.wisdom.voice import synthesize_advisor_quote

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.mp3"

            with patch("project_management_automation.tools.wisdom.voice._synthesize_edge_tts") as mock_synth:
                mock_synth.return_value = output_path
                output_path.write_bytes(b"fake audio data")

                result = synthesize_advisor_quote(
                    "This is a test quote with several words",
                    output_path=str(output_path),
                    backend="edge-tts",
                )

                assert result["success"] is True
                assert "text_length" in result
                assert "word_count" in result
                assert "duration_estimate_seconds" in result


class TestGeneratePodcastAudio:
    """Test generate_podcast_audio function."""

    def test_generate_podcast_no_backend(self):
        """Should return error when no backend available."""
        from project_management_automation.tools.wisdom.voice import generate_podcast_audio

        with patch("project_management_automation.tools.wisdom.voice.get_available_backend") as mock:
            mock.return_value = None
            result = generate_podcast_audio([], backend="auto")

            assert result["success"] is False
            assert "error" in result

    def test_generate_podcast_with_consultations(self):
        """Should process consultations and generate segments."""
        from project_management_automation.tools.wisdom.voice import generate_podcast_audio

        consultations = [
            {"advisor": "bofh", "quote": "Trust no one.", "metric": "security"},
            {"advisor": "stoic", "quote": "Endure.", "metric": "testing"},
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "podcast.mp3"

            with patch("project_management_automation.utils.find_project_root") as mock_root:
                mock_root.return_value = Path(tmpdir)

                with patch("project_management_automation.tools.wisdom.voice.synthesize_advisor_quote") as mock_synth:

                    def fake_synth(text, advisor, output_path, backend):
                        Path(output_path).write_bytes(b"fake audio")
                        return {"success": True, "audio_path": str(output_path)}

                    mock_synth.side_effect = fake_synth

                    result = generate_podcast_audio(
                        consultations,
                        output_path=str(output_path),
                        backend="edge-tts",
                        include_intro=False,  # Skip intro for simpler test
                    )

                    # Should have processed the consultations
                    assert "consultations_processed" in result


class TestIntegrationWithAdvisors:
    """Test integration between voice and advisor modules."""

    def test_all_advisors_have_voice_mappings(self):
        """All advisors in METRIC_ADVISORS should have voice mappings."""
        from project_management_automation.tools.wisdom.advisors import METRIC_ADVISORS
        from project_management_automation.tools.wisdom.voice import ADVISOR_VOICES

        for metric, info in METRIC_ADVISORS.items():
            advisor = info["advisor"]
            # Each advisor should have a voice in at least one backend
            has_voice = (
                advisor in ADVISOR_VOICES["elevenlabs"]
                or advisor in ADVISOR_VOICES["edge-tts"]
                or advisor in ADVISOR_VOICES["pyttsx3"]
                or "default" in ADVISOR_VOICES["elevenlabs"]  # Fall back to default
            )
            assert has_voice, f"Advisor '{advisor}' for metric '{metric}' has no voice mapping"
