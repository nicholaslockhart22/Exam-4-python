from kmer_context import (
    validate_sequence,
    update_kmer_count,
    count_kmers_with_context,
    write_results_to_file,
)


def test_validate_sequence_valid():
    assert validate_sequence("ATGC", 2) is True


def test_validate_sequence_too_short():
    assert validate_sequence("AT", 2) is False


def test_validate_sequence_invalid_character():
    assert validate_sequence("ATBX", 2) is False


def test_validate_sequence_rejects_numbers():
    assert validate_sequence("ATG1", 2) is False


def test_update_kmer_count_new_kmer():
    data = {}
    update_kmer_count(data, "AT", "G")

    assert data["AT"]["count"] == 1
    assert data["AT"]["next_chars"]["G"] == 1


def test_update_kmer_count_existing_kmer_same_next_char():
    data = {"AT": {"count": 1, "next_chars": {"G": 1}}}
    update_kmer_count(data, "AT", "G")

    assert data["AT"]["count"] == 2
    assert data["AT"]["next_chars"]["G"] == 2


def test_update_kmer_count_existing_kmer_different_next_char():
    data = {"AT": {"count": 1, "next_chars": {"G": 1}}}
    update_kmer_count(data, "AT", "C")

    assert data["AT"]["count"] == 2
    assert data["AT"]["next_chars"]["G"] == 1
    assert data["AT"]["next_chars"]["C"] == 1


def test_count_kmers_with_context_single_sequence():
    result = count_kmers_with_context("ATGT", 2)

    assert result["AT"]["count"] == 1
    assert result["AT"]["next_chars"]["G"] == 1
    assert result["TG"]["count"] == 1
    assert result["TG"]["next_chars"]["T"] == 1


def test_count_kmers_with_context_combines_sequences():
    data = {}
    count_kmers_with_context("ATGT", 2, data)
    count_kmers_with_context("ATGA", 2, data)

    assert data["AT"]["count"] == 2
    assert data["AT"]["next_chars"]["G"] == 2
    assert data["TG"]["count"] == 2
    assert data["TG"]["next_chars"]["T"] == 1
    assert data["TG"]["next_chars"]["A"] == 1


def test_write_results_to_file(tmp_path):
    data = {
        "AT": {"count": 2, "next_chars": {"G": 2}},
        "TG": {"count": 1, "next_chars": {"A": 1}},
    }

    output_file = tmp_path / "output.txt"
    write_results_to_file(data, output_file)

    content = output_file.read_text()

    assert "AT count:2 G:2\n" in content
    assert "TG count:1 A:1\n" in content
