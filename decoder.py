from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import random
import sys
import time

import numpy as np
from six.moves import xrange
import tensorflow as tf
from texttospeech import say
import data_utils
import seq2seq_model
from vocabulary import inputrepair, outputrepair
from inputManager import read_input, cliche
from instruction import Execution

try:
    reload
except NameError:
    pass
else:
    reload(sys).setdefaultencoding('utf-8')

try:
    from ConfigParser import SafeConfigParser
except:
    from configparser import SafeConfigParser  # In Python 3, ConfigParser has been renamed to configparser for PEP 8 compliance.


def create_model(
    session,
    forward_only,
    gConfig,
    use_lstm=False,
    ):
    """Create model and initialize or load parameters"""

    model = seq2seq_model.Seq2SeqModel(
        gConfig['enc_vocab_size'],
        gConfig['dec_vocab_size'],
        _buckets,
        gConfig['layer_size'],
        gConfig['num_layers'],
        gConfig['max_gradient_norm'],
        gConfig['batch_size'],
        gConfig['learning_rate'],
        gConfig['learning_rate_decay_factor'],
        forward_only=forward_only,
        use_lstm=use_lstm
        )

    if 'pretrained_model' in gConfig:
        model.saver.restore(session, gConfig['pretrained_model'])
        return model

    ckpt = tf.train.get_checkpoint_state(gConfig['working_directory'])

  # the checkpoint filename has changed in recent versions of tensorflow

    checkpoint_suffix = ''
    if tf.__version__ > '0.12':
        checkpoint_suffix = '.index'
    if ckpt and tf.gfile.Exists(ckpt.model_checkpoint_path
                                + checkpoint_suffix):
        print('Reading model parameters from %s'
              % ckpt.model_checkpoint_path)
        model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        print('Created model with fresh parameters.')
        session.run(tf.initialize_all_variables())
    return model


def get_config(config_file='seq2seqperform.ini'):
    parser = SafeConfigParser()
    parser.read(config_file)

    # get the ints, floats and strings

    _conf_ints = [(key, int(value)) for (key, value) in
                  parser.items('ints')]
    _conf_floats = [(key, float(value)) for (key, value) in
                    parser.items('floats')]
    _conf_strings = [(key, str(value)) for (key, value) in
                     parser.items('strings')]
    return dict(_conf_ints + _conf_floats + _conf_strings)


_buckets = [(5, 10), (10, 15), (20, 25), (40, 50)]


def decode():

    PERFORM = True

    gConfig = get_config()
    chatConfig = get_config('seq2seq.ini')
  # Only allocate part of the gpu memory when predicting.

    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.2)
    config = tf.ConfigProto(gpu_options=gpu_options)
    graph = tf.Graph()
    chat_graph = tf.Graph()
    chat_session = tf.Session(config=config, graph=chat_graph)
    sess = tf.Session(config=config, graph=graph)
    model = None
    chatmodel = None
    # Ceate model and load parameters.
    with graph.as_default():
        model = create_model(sess, True, use_lstm=False, gConfig = gConfig)
    with chat_graph.as_default():
        chatmodel = create_model(chat_session, True, use_lstm=True, gConfig=chatConfig)
    say('Loaded required models. Ready')
    model.batch_size = 1  # We decode one sentence at a time.
    chatmodel.batch_size = 1
    # Lad vocabularies.
    enc_vocab_path = os.path.join(gConfig['working_directory'],
            'vocab%d.enc' % gConfig['enc_vocab_size'])
    dec_vocab_path = os.path.join(gConfig['working_directory'],
            'vocab%d.dec' % gConfig['dec_vocab_size'])
    # Lad Chat vocabularies
    chat_enc_vocab_path = \
        os.path.join(chatConfig['working_directory'], 'vocab%d.enc'
                     % chatConfig['enc_vocab_size'])
    chat_dec_vocab_path = \
        os.path.join(chatConfig['working_directory'], 'vocab%d.dec'
                     % chatConfig['dec_vocab_size'])
    (enc_vocab, _) = \
        data_utils.initialize_vocabulary(enc_vocab_path)
    (dec_vocab, rev_dec_vocab) = \
        data_utils.initialize_vocabulary(dec_vocab_path)
    (chat_enc_vocab, _) = \
        data_utils.initialize_vocabulary(chat_enc_vocab_path)
    (chat_dec_vocab, chat_rev_dec_vocab) = \
        data_utils.initialize_vocabulary(chat_dec_vocab_path)
    # Decode from standard input.
    sentences, chat_sentence = read_input()
    """ 
    .
    .
    Program loop start 
    .
    .
    """
    while True:
        for sentence in sentences:
            if (not PERFORM) and (sentence == "chatbot off" or sentence == "stop chatbot" or sentence == "start working"or sentence == "stop chat"):
                PERFORM = True
                break
        
            if sentence == "terminate session" or sentence == "terminate this session":
                return
        
            if not PERFORM:
                sentence = chat_sentence
            
            #print("SENTENCE stage 1: "+sentence)
            if PERFORM:
                (sentence, Hash) = inputrepair(sentence, enc_vocab)
            #print("SENTENCE stage 2: "+sentence)
                     # Get token-ids for the input sentence.
            token_ids = \
                data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence),
                    enc_vocab)
            chat_token_ids = \
                data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence),
                    chat_enc_vocab)
                     # Which bucket does it belong to?
            bucket_id = min([b for b in xrange(len(_buckets))
                            if _buckets[b][0] > len(token_ids)])
            chat_bucket_id = min([b for b in xrange(len(_buckets))
                            if _buckets[b][0] > len(chat_token_ids)])
                    # Get a 1-element batch to feed the sentence to the model.
            if PERFORM:
                (encoder_inputs, decoder_inputs, target_weights) = \
                    model.get_batch({bucket_id: [(token_ids, [])]},
                                    bucket_id)
                    # Get output logits for the sentence.
                (_, _, output_logits) = model.step(
                    sess,
                    encoder_inputs,
                    decoder_inputs,
                    target_weights,
                    bucket_id,
                    True,
                    )
            else:
                (chat_encoder_inputs, chat_decoder_inputs,
                 chat_target_weights) = \
                    chatmodel.get_batch({bucket_id: [(chat_token_ids, [])]},
                        chat_bucket_id)
                (_, _, output_logits) = chatmodel.step(
                    chat_session,
                    chat_encoder_inputs,
                    chat_decoder_inputs,
                    chat_target_weights,
                    chat_bucket_id,
                    True,
                    )
                    # This is a greedy decoder - outputs are just argmaxes of output_logits.
            outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
                    # If there is an EOS symbol in outputs, cut them at that point.
            if data_utils.EOS_ID in outputs:
                outputs = outputs[:outputs.index(data_utils.EOS_ID)]
                    # print(Hash)
            if PERFORM:
                output = ' '.join([tf.compat.as_str(rev_dec_vocab[output]) for output in outputs])
                output = outputrepair(output, Hash)
                task = Execution(output)
                status = task.execute()
            else:
                output = ' '.join([tf.compat.as_str(chat_rev_dec_vocab[output]) for output in outputs])
                say(output)
            if status == 1:
                state = True
            else:
                state = False
            if status == 2:
                PERFORM = False
        sentences, chat_sentence = read_input(state)
if __name__ == '__main__':
    """
    try:
        decode()
    except Exception as e:
        print("System encountered some error. Exiting.\n"+str(e))
    """
    decode()